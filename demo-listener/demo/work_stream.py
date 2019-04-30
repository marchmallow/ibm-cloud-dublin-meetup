# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

import traceback
from datetime import datetime, timedelta
import redis
from rx import Observable
from .query_processing_exception import QueryProcessingException


def create_work_stream(cfg, logger, api_imp, post_process_imp):
    return RedisWorkStream(cfg, logger, api_imp, post_process_imp)


class RedisWorkStream(object):
    """
        A WorkStream implentation that takes task out of a Redis queue and sends
        each to a `work` function. The goal of the WorkStream is to isolate
        the `work` function away from the Queueing system.
    """

    wait_q_name = None
    work_q_name = None
    work_q_ttl_name = None
    backlog_q_name = None
    wait_q_amount = 1
    cfg = None
    logger = None
    api_imp = None
    post_process_imp = None

    task_count = 0
    task_capacity = 3
    task_poll_rate = 1000
    task_ttl = 10

    def __init__(self, cfg, logger, api_imp, post_process_imp):
        """ Initializing queue """
        self.cfg = cfg
        self.logger = logger
        self.api_imp = api_imp
        self.post_process_imp = post_process_imp

        host = self.cfg.QUEUE_CONFIG['redis']['host']
        port = self.cfg.QUEUE_CONFIG['redis']['port']
        db = self.cfg.QUEUE_CONFIG['redis']['db']
        passwd = self.cfg.QUEUE_CONFIG['redis']['password']
        redis_ssl = self.cfg.QUEUE_CONFIG['redis']['ssl']

        self.logger.info('Connecting to Redis at {}:{}/{}'.format(host, port, db))
        self.r = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            password=passwd,
            charset="utf-8", decode_responses=True,
            ssl=redis_ssl,
            ssl_cert_reqs=u'none')

        self.task_capacity = self.cfg.TASK_CAPACITY
        self.task_poll_rate = self.cfg.TASK_POLL_RATE
        self.wait_q_name = self.cfg.QUEUE_CONFIG['redis']['wait_queue']
        self.work_q_name = self.cfg.QUEUE_CONFIG['redis']['work_queue']


        logger.debug('Wait queue: {}'.format(self.wait_q_name))
        logger.debug('Work queue: {}'.format(self.work_q_name))


    def join(self):
        return Observable.timer(
            datetime.now(),
            self.task_poll_rate
        ).filter(
            lambda _: not self._at_capacity()
        ).map(
            lambda _: self._take_task()
        ).filter(
            lambda task: task is not None
        ).flat_map(
            lambda task: self._do_work(task)
        ).map(
            lambda task : self._mark_done(task)
        )


    def _at_capacity(self):
        tasks_in_queue = self.r.llen(self.work_q_name)
        return tasks_in_queue >= self.task_capacity


    def _take_task(self):

        self._log_pending_tasks()

        queue_name = '{}_{}'.format(self.wait_q_name, '0')
        queue_length = self.r.llen(queue_name)
        if(queue_length != 0):
            task_str = self.r.rpoplpush(queue_name, self.work_q_name)
            self.logger.info('Atomically moved task {} [{} => {}]'.format(task_str, queue_name, self.work_q_name))
            return task_str


        return None


    def _delete_task(self, task):

        task_str = str(task).replace("'", '"')

        self.logger.info('Removing task {} from the {} queue...'.format(task_str, self.work_q_name))
        r_count = self.r.lrem(self.work_q_name, -1, task_str)

        if r_count == 0:
            self.logger.warn('Nothing removed from work queue for task {}'.format(task))

        return task


    def _do_work(self, task):
        self.logger.info('Starting {}...'.format(task))

        return Observable.just(
            task
        ).map(
            lambda task: self.post_process_imp.putTaskToPostgreSQL(task)
        ).catch_exception(
            lambda error: self._logErrorAndResume(error, task)
        )


    def _mark_done(self, task):
        self.logger.info('Marking done {}...'.format(task))

        self._delete_task(task)

        return task


    def _logErrorAndResume(self, error, task):

        self.logger.error("Failed processing task {}. Reason: {}:{}".format(task, error.__class__.__name__, error))
        try:
            if error.__class__.__name__ == QueryProcessingException.__name__:
                self._notify_task(task, "ERROR", error.get_status())
            else:
                self._notify_task(task, "ERROR")
        except:
            traceback.print_exc()

        return Observable.empty()


    def _notify_task(self, task, status, task_state=None):
        self.logger.debug('Notify task {} status {} task_state {}'.format(task, status, task_state))
        if status == 'ERROR':
            # Delete the failed task from work queue

            self._delete_task(task)

        return task

    def _log_pending_tasks(self, dump_tasks=False):

        task_total = self.r.llen(self.work_q_name)
        for queue_number in range(0, self.wait_q_amount):
            queue_name = '{}_{}'.format(self.wait_q_name, queue_number)
            task_total += self.r.llen(queue_name)
        task_total += self.r.llen(self.backlog_q_name)

        self.logger.info('Total number of tasks:[{}]'.format(task_total))

        self._log_queue(self.work_q_name, dump_tasks)
        self._log_queue(self.work_q_ttl_name, dump_tasks)

        for queue_number in range(0, self.wait_q_amount):
            queue_name = '{}_{}'.format(self.wait_q_name, queue_number)
            self._log_queue(queue_name, dump_tasks)

        self._log_queue(self.backlog_q_name, dump_tasks)


    def _log_queue(self, queue_name, dump_tasks=False):
        queue_length = self.r.llen(queue_name)
        self.logger.info('..queue [{}] has [{}] tasks to process.'.format(queue_name, queue_length))

        if(dump_tasks):
            elements = self.r.lrange(queue_name, 0, -1)
            for e in elements:
                self.logger.debug("....task [{}]".format(e))
