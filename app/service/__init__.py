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
import time

from app.service.translate import translate_task, task_error
import threading

sleep_time = 0


def thread_loop():
    while True:
        progress = None
        try:
            progress = translate_task()
        except Exception as e:
            print(f"[Error] translate_task() {progress}: {e} ")
            try:
                task_error(progress)
            except Exception as e:
                print(f"[Error] task_error() {progress}: {e} ")

        if sleep_time != 0:
            time.sleep(sleep_time)


thread = threading.Thread(target=thread_loop)
thread.setDaemon(True)
thread.start()
print(f"Sync task{i} is running now.")
