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

import unittest

from app.forum.get import get_post_ids, get_post, get_topics, get_topic_and_post_ids
from app.forum.create import  client


class TestCNForum(unittest.TestCase):

    def test_get_topic(self):
        print(get_post_ids(1009793))

    def test_get_post(self):
        print(get_post(1183484))

    def test_get_topics(self):
        print(get_topics(1))

    def test_get_topic_and_post_ids(self):
        topic, post_ids = get_topic_and_post_ids(1009793)
        print(topic)
        print(post_ids)

    def test_solve(self):
        client.solve_solution(983152)
