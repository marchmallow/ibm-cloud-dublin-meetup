# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

"""
Demo Listener
Usage:
    demo-listener [options]
Options:
    -h --help                   Show this screen.
"""
from demo.app import Worker
from demo import config
from .logger import logger
from demo.api_imp import Demo
from demo.post_process_imp import DemoPostProcess


def main():
    psql = DemoPostProcess(logger, config)
    worker = Worker(Demo, psql, config, logger)
    worker.start()


if __name__ == "__main__":
    # execute only if run as a script
    main()
