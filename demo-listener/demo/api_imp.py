# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0


from datetime import timedelta


class Demo():

    def __init__(self, cfg, logger, redis_stream=None):
        self.cfg = cfg
        self.logger = logger
        self.redis_stream = redis_stream
