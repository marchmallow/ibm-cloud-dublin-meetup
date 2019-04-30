# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import psycopg2
import datetime


class DemoPostProcess(object):

    conn = None
    cur = None

    def __init__(self, logger, cfg):
        self.logger = logger
        self.cfg = cfg




    def putTaskToPostgreSQL(self, task):
        try:
            self.conn = psycopg2.connect(dbname=self.cfg.DB_CONFIG['psql']['db'], user=self.cfg.DB_CONFIG['psql']['user'],
                host=self.cfg.DB_CONFIG['psql']['host'], password=self.cfg.DB_CONFIG['psql']['password'], port=self.cfg.DB_CONFIG['psql']['port'])

            self.cur = self.conn.cursor()
            self.logger.info("Pushing task [{}] to the database!".format(task))
            st = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute("INSERT INTO meetup.example (ts, task) VALUES (%s, %s)",(st, task))
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as err:
            print("I am unable to connect to the database. {}".format(err))

        return task
