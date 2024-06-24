# Copyright 2022 PingCAP, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
import logging
from app.config import conf


def getLogger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logLevel = logging.DEBUG if conf.debug else logging.INFO
    logger.setLevel(logLevel)

    # Create handlers for logging to the standard output and a file
    stdoutHandler = logging.StreamHandler(stream=sys.stdout)
    fileHandler = logging.FileHandler(conf.log_path)

    # Set the log levels on the handlers
    stdoutHandler.setLevel(logLevel)
    fileHandler.setLevel(logLevel)

    # Create a log format using Log Record attributes
    fmt = logging.Formatter(
        "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
    )

    # Set the log format on each handler
    stdoutHandler.setFormatter(fmt)
    fileHandler.setFormatter(fmt)

    # Add each handler to the Logger object
    logger.addHandler(stdoutHandler)
    logger.addHandler(fileHandler)

    return logger
