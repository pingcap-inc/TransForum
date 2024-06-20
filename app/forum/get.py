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
from typing import List

import requests
from sqlalchemy.orm import Session
from app.db.gen_instances import CnTopics, CnPosts, SyncProgress
from app.db import db_exec
from dataclasses import fields
from retrying import retry


def get_topic_and_post_ids(topic_id: int) -> (CnTopics, List[int]):
    r = requests.get(f"https://asktug.com/t/topic/{topic_id}.json")
    topic = r.json()
    posts = topic['post_stream']['posts']
    topic['has_accepted_answer'] = topic.get('accepted_answer') is not None

    posts_without_empty = list(filter(lambda post: post['cooked'] != "", posts))
    return dict_to_topic(topic), [post['id'] for post in posts_without_empty]


def get_post_ids(topic_id: int) -> List[int]:
    r = requests.get(f"https://asktug.com/t/{topic_id}/posts.json")
    posts = r.json()['post_stream']['posts']
    posts_without_empty = list(filter(lambda post: post['cooked'] != "", posts))

    return [post['id'] for post in posts_without_empty]


def get_post(post_id: int) -> CnPosts:
    r = requests.get(f"https://asktug.com/posts/{post_id}.json")
    post = r.json()
    post['en_id'] = -1
    post['translated'] = ''

    return dict_to_post(post)


def get_topics(page: int) -> List[CnTopics]:
    r = requests.get(f"https://asktug.com/latest.json?order=created&page={page}")
    topics = r.json()['topic_list']['topics']

    return [dict_to_topic(topic) for topic in topics]


def dict_to_post(data_dict: dict):
    data_dict['en_id'] = -1
    data_dict['translated'] = ''
    return _from_dict(CnPosts, data_dict)


def dict_to_topic(data_dict: dict):
    data_dict['en_id'] = -1
    data_dict['translated_title'] = ''
    return _from_dict(CnTopics, data_dict)


def _from_dict(data_class, data_dict: dict):
    field_set = {f.name for f in fields(data_class)}
    filtered_data = {k: v for k, v in data_dict.items() if k in field_set}
    return data_class(**filtered_data)


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def get_and_save_page_sync_progress(page: int, earliest: datetime) -> bool:
    """
    Save topic ids to sync_progress
    :param earliest: the earliest time need to be synced
    :param page: page number
    :return: has next page
    """

    # we use create time as the order to query the topics by page
    topics = get_topics(page)
    topics = list(filter(lambda t: datetime.datetime.strptime(t.created_at, '%Y-%m-%dT%H:%M:%S.%fZ') > earliest, topics))
    save_page_topic_ids(topics)
    print(f"Got {len(topics)} topics in page {page}!")
    return len(topics) != 0


@db_exec
def save_page_topic_ids(session: Session, topics: List[CnTopics]):
    for topic in topics:
        sync_progress = session.get(SyncProgress, topic.id)
        if sync_progress is None:
            session.add(SyncProgress(
                cn_topic_id=topic.id,
                en_topic_id=None,
                cn_title=topic.title,
                cn_created_at=topic.created_at,
                translate_state=None,
                translate_at=None
            ))


def save_all_topic_ids(earliest: datetime):
    page_index = 0
    has_next = get_and_save_page_sync_progress(page_index, earliest)
    while has_next:
        page_index = page_index + 1
        has_next = get_and_save_page_sync_progress(page_index, earliest)
