# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

from demo.work_stream import create_work_stream


class Worker(object):
    cfg = None
    work_stream = None
    logger = None

    def __init__(self, api_imp, post_process_imp, cfg, logger):
        """ Initializing demo listener  """
        self.cfg = cfg
        self.logger = logger
        self.work_stream = create_work_stream(cfg, logger, api_imp, post_process_imp)

    def start(self):

        """ Main hook to start the worker."""
        self.logger.info('Started demo listener for {}'.format(self.cfg.TYPE))

        self.work_stream.join().to_blocking().last().subscribe(
            on_completed=lambda: self.logger.info('Done'),
            on_next=lambda task: self.logger.info("Finished task {}".format(task)),
            on_error=print)

    def stop(self, signal):
        """ A hook to when a worker starts shutting down. """
        self.logger.info('Stopped listenerCommon for {}'.format(self.cfg.TYPE))
        pass
