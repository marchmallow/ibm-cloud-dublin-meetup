# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

import logging
from logging.config import dictConfig

from .config import LOGGING

dictConfig(LOGGING)
logger = logging.getLogger('listener')