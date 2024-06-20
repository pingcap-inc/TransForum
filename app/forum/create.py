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

from app.forum.client import DiscourseClientWithPlugins
from app.config import conf
from app.db.gen_instances import CnTopics, CnPosts

client = DiscourseClientWithPlugins(
        conf.en_discourse_host,
        api_username=conf.en_discourse_api_username,
        api_key=conf.en_discourse_api_key)


def topic_post_format(topic: CnTopics, post: CnPosts) -> str:
    avatar_url = post.avatar_template.replace("{size}", "120")
    return f"""
> **Note:**
> This topic has been translated from a Chinese forum by GPT and might contain errors.
>
> Original topic: [{topic.title}](https://asktug.com/t/topic/{topic.id})

<div>
    <img class="avatar" width="48" height="48" src="https://asktug.com{avatar_url}" /> |
    username: <a href="https://asktug.com/u/{post.username}">{post.username}</a>
</div>

--------

{post.translated}
"""


def post_format(topic: CnTopics, post: CnPosts) -> str:
    avatar_url = post.avatar_template.replace("{size}", "120")

    return f"""
<div>
    <img class="avatar" width="48" height="48" src="https://asktug.com{avatar_url}" /> |
    username: <a href="https://asktug.com/u/{post.username}">{post.username}</a> |
    <a href="https://asktug.com/t/topic/{topic.id}/{post.post_number}">Original post link</a>
</div>

------

{post.translated}
"""


def create_topic(topic: CnTopics, post: CnPosts):
    return client.create_post(
        category_id=conf.en_discourse_category_id,
        title=topic.translated_title,
        content=topic_post_format(topic, post)
    )


def create_post(topic: CnTopics, post: CnPosts):
    """
    Before you all this function, you should call `create_topic` first.
    And save the `en_id` of the topic, it will be used in this function
    :param topic: A CnTopics instance and set `en_id`
    :param post: the post you want to save
    :return: post
    """

    return client.create_post(
        topic_id=topic.en_id,
        content=post_format(topic, post),
        reply_to_post_number=post.reply_to_post_number
    )


def update_topic(topic: CnTopics):
    topic_url = f"{conf.en_discourse_host}/t/{topic.en_id}"
    return client.update_topic(topic_url, topic.translated_title)


def update_post(topic: CnTopics, post: CnPosts):
    if post.post_number == 1:
        # It's a post that published with topic
        content = topic_post_format(topic, post)
    else:
        content = post_format(topic, post)

    return client.update_post(post.en_id, content=content)
