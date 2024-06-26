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
import datetime
import time

from app.service.translate import translate_task, task_error, translate_or_update_first_page
import threading
from app.config import conf
from app.log import getLogger

logger = getLogger(__name__)


def thread_loop():
    while True:
        try:
            incremental_loop()
        except Exception as e:
            logger.error(f"[Error {datetime.datetime.now()}] translate_or_update_first_page() {e}")

        if conf.sleep_time != 0:
            time.sleep(conf.sleep_time)


def incremental_loop():
    translate_or_update_first_page()


thread = threading.Thread(target=thread_loop)
thread.setDaemon(True)
thread.start()
logger.info(f"Sync task is running now.")
