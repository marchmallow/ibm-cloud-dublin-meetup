# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

import redis
import os

class RedisStream(object):

    redis_endpoint = None
    redis_port = None
    redis_db = None
    redis_password = None
    redis_ssl = None
    conn = None


    def __init__(self):
      self.redis_endpoint = os.environ.get('REDIS_HOST')
      self.redis_port = int(os.environ.get('REDIS_PORT'))
      self.redis_db = os.environ.get('REDIS_DB', "0")
      self.redis_password = os.environ.get('REDIS_PASSWORD')
      self.redis_ssl = (os.environ.get('REDIS_SSL', 'true').lower() in ('true'))
      self.conn = redis.StrictRedis(
        host=self.redis_endpoint,
        port=self.redis_port,
        password=self.redis_password,
        ssl=self.redis_ssl,
        ssl_cert_reqs=u'none')





    def pushTask(self, queue, task):
        try:
            self.conn.rpush(queue, task)
        except Exception as ex:
            print('Error:', ex)
            exit('Failed to connect, terminating.')
