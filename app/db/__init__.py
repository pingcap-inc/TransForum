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

from sqlalchemy import URL, create_engine
from app.config import conf
from sqlalchemy.orm import Session
from typing import Callable, Any
from app.log import getLogger

logger = getLogger(__name__)


def get_db_url():
    if conf.debug:
        return URL(
            drivername="mysql+pymysql",
            username=conf.tidb_user,
            password=conf.tidb_password,
            host=conf.tidb_host,
            port=conf.tidb_port,
            database=conf.tidb_db_name,
            query={}
        )

    return URL(
        drivername="mysql+pymysql",
        username=conf.tidb_user,
        password=conf.tidb_password,
        host=conf.tidb_host,
        port=conf.tidb_port,
        database=conf.tidb_db_name,
        query={"ssl_verify_cert": True, "ssl_verify_identity": True},
    )


# TiDB Serverless clusters have a limitation: if there are no active connections for 5 minutes,
# they will shut down, which closes all connections, so we need to recycle the connections
engine = create_engine(get_db_url(), pool_recycle=100, pool_pre_ping=True)


def db_exec(func: Callable[[Session], None]):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            try:
                func(session, *args, **kwargs)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Exec and an error occurred: {e}")
                raise
    return wrapper


def db_query(func: Callable[[Session], Any]):
    def wrapper(*args, **kwargs) -> Any:
        with Session(engine) as session:
            try:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                logger.error(f"Query and an error occurred: {e}")
                raise
    return wrapper

