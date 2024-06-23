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
from typing import List

from app.forum.get import get_topic_and_post_ids, get_post, get_recent_updated_topics
from app.forum.create import create_post, create_topic, update_post, update_topic, client
from enum import Enum
from app.db import db_query, db_exec, engine
from sqlalchemy.orm import Session
from app.db.gen_instances import CnTopics, CnPosts, SyncProgress
from app.models.openai_client import translate, translate_title
from lxml import etree
from datetime import datetime
import re
import logging


logger = logging.getLogger(__name__)


class Operator(Enum):
    Nothing = 1
    Update = 2
    Create = 3


def translate_topic(topic_id: int):
    topic, post_ids = get_topic_and_post_ids(topic_id)
    topic_op = translate_and_save_topic(topic)

    if topic_op == Operator.Create:
        posts = [get_post(post_id) for post_id in post_ids]
        post_ops = [translate_and_save_post(post) for post in posts]
        topic_post = posts[0]

        topic_result = create_topic(topic, topic_post)
        logger.debug(f"topic_result: {topic_result}")

        topic.en_id = topic_result['topic_id']
        topic_post.en_id = topic_result['id']
        update_obj(topic)
        update_obj(topic_post)

        for i in range(1, len(posts)):
            if post_ops[i] == Operator.Create:
                post_result = create_post(topic, posts[i])
                logger.debug(f"post_result: {post_result}")
                posts[i].en_id = post_result['id']
                update_obj(posts[i])

                if posts[i].accepted_answer:
                    client.solve_solution(posts[i].en_id)

        print(f"Create topic {topic.id} successfully")
    else:
        if topic_op == Operator.Update:
            update_topic(topic)

        # update posts, no matter the topic will be updated or not
        posts = [get_post(post_id) for post_id in post_ids]
        post_ops = [translate_and_save_post(post) for post in posts]
        for i in range(len(posts)):
            if post_ops[i] == Operator.Update:
                update_post(topic, posts[i])
            elif post_ops[i] == Operator.Create:
                post_result = create_post(topic, posts[i])
                print(f"post_result: {post_result}")
                posts[i].en_id = post_result['id']
                update_obj(posts[i])

        print(f"Update topic {topic.id} successfully")

    print(f"topic en id: {topic.en_id}")

    return topic


@db_exec
def update_obj(session: Session, obj):
    session.merge(obj)


@db_query
def translate_and_save_post(session: Session, post: CnPosts) -> Operator:
    op = Operator.Nothing
    old_post = session.query(CnPosts).filter(CnPosts.id == post.id).first()

    if old_post is not None and compare_date_almost_same(old_post.updated_at, post.updated_at):
        return op

    changed_raw = change_markdown_pic_to_link(post.raw, post.cooked)
    translated = translate(changed_raw)
    post.translated = translated
    op = Operator.Create

    if old_post is not None:
        post.en_id = old_post.en_id
        op = Operator.Update

    session.merge(post)
    return op


@db_query
def translate_and_save_topic(session: Session, topic: CnTopics) -> Operator:
    op = Operator.Nothing
    old_topic = session.query(CnTopics).filter(CnTopics.id == topic.id).first()
    if old_topic is not None:
        return op

    # new topic or need to update
    # topic's title should not exceed 255 chars
    topic.translated_title = translate_title(topic.title)
    op = Operator.Create
    if old_topic is not None:
        topic.en_id = old_topic.en_id
        op = Operator.Update

    session.merge(topic)
    return op


def change_markdown_pic_to_link(raw: str, cooked: str) -> str:
    """
    Change markdown's pic to the link of CN forum
    :param raw: post's raw markdown, might contain like: ![image|690x301](upload://b5xMkedGUmYoz1roDGsL7xt29yT.png)
    :param cooked: post's cooked HTML, will have correspoding picture link.
    :return: changed raw string
    """
    img_pattern = re.compile(r'!\[([^\]]+)\]\(upload://([^\)]+)\.([a-zA-Z]+)\)')

    def replacer(match):
        description = match.group(1)  # match description
        image_sha = match.group(2)      # match the SHA of the image

        new_url = find_link_from_cooked(cooked, image_sha)
        if not new_url.startswith("http"):
            new_url = f"https://asktug.com/uploads{new_url}"
        return f'![{description}]({new_url})'

    replaced_raw = img_pattern.sub(replacer, raw)
    return replaced_raw


def find_link_from_cooked(cooked: str, sha: str) -> str:
    src_sets = etree.HTML(cooked).xpath(f"//img[@data-base62-sha1='{sha}']/@srcset")
    if len(src_sets) == 0:
        src = etree.HTML(cooked).xpath(f"//img[@data-base62-sha1='{sha}']/@src")
        if len(src) == 0:
            raise Exception("Cannot find the picture link")
        else:
            print(str(src[0]))
            return str(src[0])

    src_set = str(src_sets[0])
    # srt_set will look like: https://xxxxxxxxx.png, https://xxxxxxxxx.png 1.5x, https://xxxxxxxxx.png 2x
    # we want to get the last one, but not contain the 2x or something else.
    link = src_set.split(sep=", ")[-1].split(sep=" ")[0]

    return link


def compare_date_almost_same(old_update: datetime, new_update: str) -> bool:
    new_update_datetime = datetime.strptime(new_update, '%Y-%m-%dT%H:%M:%S.%fZ')
    delta = (old_update - new_update_datetime).total_seconds()
    if delta < 0:
        delta = delta * -1

    return delta <= 2


@db_exec
def task_error(session: Session, progress: SyncProgress):
    if progress is not None:
        progress.en_topic_id = -1
        session.merge(progress)


@db_query
def query_progress_and_update_state_to_translating(session: Session):
    progress = session.query(SyncProgress)\
        .filter(SyncProgress.translate_state == 0)\
        .order_by(SyncProgress.cn_created_at.desc()).first()

    if progress is None:
        print("All synchronized")
        return None

    progress.translate_state = 1
    session.merge(progress)
    session.expunge(progress)
    return progress


@db_exec
def save_progress(session: Session, sync_progress, topic):
    sync_progress.en_topic_id = topic.en_id
    sync_progress.translate_at = datetime.now()
    sync_progress.translate_state = 2
    session.merge(sync_progress)


def translate_task(wait_when_none: int = 2):
    sync_progress = query_progress_and_update_state_to_translating()
    print(f"sync_progress: {sync_progress}")

    if sync_progress is None:
        if wait_when_none != 0:
            time.sleep(wait_when_none)
        return

    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] get {sync_progress}")

    topic = translate_topic(sync_progress.cn_topic_id)
    save_progress(sync_progress, topic)

    delta = datetime.now() - start_time
    print(f"[{delta.seconds}s] merged {sync_progress}")

    return sync_progress


def translate_or_update_first_page(page: int = 0):
    topics = get_recent_updated_topics(page)
    for topic in topics:
        topic_id = topic.id
        translate_topic(topic_id=topic_id)
