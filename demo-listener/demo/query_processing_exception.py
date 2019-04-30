# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

class QueryProcessingException(Exception):
    def __init__(self, text, status):
        super().__init__(text)
        self.status = status
        self.text = text

    def get_status(self):
        return self.status



