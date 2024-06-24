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

from dotenv import load_dotenv
import os


class __Config:
    def __init__(self):
        load_dotenv()

        self.debug = bool(os.getenv("DEBUG", "True") == "True")
        self.log_path = os.getenv("LOG_PATH", "./transforum.log")
        self.sleep_time = int(os.getenv("SLEEP_TIME", "30"))

        self.sentry_dsn = os.getenv("SENTRY_DSN")

        self.open_ai_base_url = os.getenv("OPEN_AI_BASE_URL", "https://api.openai.com/v1")
        self.open_ai_api = os.getenv("OPEN_AI_API", "")

        self.tidb_host = os.getenv("TIDB_HOST", "127.0.0.1")
        self.tidb_port = int(os.getenv("TIDB_PORT", "4000"))
        self.tidb_user = os.getenv("TIDB_USER", "root")
        self.tidb_password = os.getenv("TIDB_PASSWORD", "")
        self.tidb_db_name = os.getenv("TIDB_DB_NAME", "test")

        self.en_discourse_host = os.getenv("EN_DISCOURSE_HOST", "")
        self.en_discourse_api_username = os.getenv("EN_DISCOURSE_API_USERNAME", "")
        self.en_discourse_api_key = os.getenv("EN_DISCOURSE_API_KEY", "")
        self.en_discourse_category_id = int(os.getenv("EN_DISCOURSE_CATEGORY_ID"))


conf = __Config()
