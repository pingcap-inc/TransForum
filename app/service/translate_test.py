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

from app.service.translate import find_link_from_cooked, change_markdown_pic_to_link

test_HTML = """
<p>
<div class="lightbox-wrapper">
   <a class="lightbox" href="https://asktug.com/uploads/default/original/4X/4/d/b/4db85f1e2110043e7e62f7785ef03bbcb6d79d77.png" data-download-href="https://asktug.com/uploads/default/4db85f1e2110043e7e62f7785ef03bbcb6d79d77" title="image">
      <img src="https://asktug.com/uploads/default/optimized/4X/4/d/b/4db85f1e2110043e7e62f7785ef03bbcb6d79d77_2_690x301.png" alt="image" data-base62-sha1="b5xMkedGUmYoz1roDGsL7xt29yT" width="690" height="301" srcset="https://asktug.com/uploads/default/optimized/4X/4/d/b/4db85f1e2110043e7e62f7785ef03bbcb6d79d77_2_690x301.png, https://asktug.com/uploads/default/optimized/4X/4/d/b/4db85f1e2110043e7e62f7785ef03bbcb6d79d77_2_1035x451.png 1.5x, https://asktug.com/uploads/default/original/4X/4/d/b/4db85f1e2110043e7e62f7785ef03bbcb6d79d77.png 2x" data-dominant-color="1C2426">
      <div class="meta">
         <svg class="fa d-icon d-icon-far-image svg-icon" aria-hidden="true">
            <use href="#far-image"></use>
         </svg>
         <span class="filename">image</span><span class="informations">1204×526 37.4 KB</span>
         <svg class="fa d-icon d-icon-discourse-expand svg-icon" aria-hidden="true">
            <use href="#discourse-expand"></use>
         </svg>
      </div>
   </a>
</div>
<br>我的缓存击中这么低</p>
"""

test_HTML2 = """<p>【 TiDB 使用环境】生产环境<br>\n【 TiDB 版本】5.2.3<br>\ntiup cluster reload tidb-cluster 报错<br>\n<div class=\"lightbox-wrapper\"><a class=\"lightbox\" href=\"https://asktug.com/uploads/default/original/4X/b/4/8/b48d27476c4600a796f63b93b4a4a87117e47135.png\" data-download-href=\"https://asktug.com/uploads/default/b48d27476c4600a796f63b93b4a4a87117e47135\" title=\"image\"><img src=\"https://asktug.com/uploads/default/optimized/4X/b/4/8/b48d27476c4600a796f63b93b4a4a87117e47135_2_690x177.png\" alt=\"image\" data-base62-sha1=\"pLemBcJpObvh3HquxOUg6S8yabP\" width=\"690\" height=\"177\" srcset=\"https://asktug.com/uploads/default/optimized/4X/b/4/8/b48d27476c4600a796f63b93b4a4a87117e47135_2_690x177.png, https://asktug.com/uploads/default/optimized/4X/b/4/8/b48d27476c4600a796f63b93b4a4a87117e47135_2_1035x265.png 1.5x, https://asktug.com/uploads/default/optimized/4X/b/4/8/b48d27476c4600a796f63b93b4a4a87117e47135_2_1380x354.png 2x\" data-dominant-color=\"060504\"><div class=\"meta\"><svg class=\"fa d-icon d-icon-far-image svg-icon\" aria-hidden=\"true\"><use href=\"#far-image\"></use></svg><span class=\"filename\">image</span><span class=\"informations\">1797×461 28.5 KB</span><svg class=\"fa d-icon d-icon-discourse-expand svg-icon\" aria-hidden=\"true\"><use href=\"#discourse-expand\"></use></svg></div></a></div></p>"""

expected = "https://asktug.com/uploads/default/original/4X/4/d/b/4db85f1e2110043e7e62f7785ef03bbcb6d79d77.png"

test_raw = """
![image|690x301](upload://b5xMkedGUmYoz1roDGsL7xt29yT.png)
我的缓存击中这么低
"""

expected_raw = """
![image|690x301](https://asktug.com/uploads/default/original/4X/4/d/b/4db85f1e2110043e7e62f7785ef03bbcb6d79d77.png)
我的缓存击中这么低
"""


class TestTranslate(unittest.TestCase):

    def test_find_link_from_cooked(self):
        result = find_link_from_cooked(test_HTML, "b5xMkedGUmYoz1roDGsL7xt29yT")
        self.assertEqual(expected, result)

        result = find_link_from_cooked(test_HTML2, "pLemBcJpObvh3HquxOUg6S8yabP")
        print(result)

    def test_change_markdown_pic_to_link(self):
        result = change_markdown_pic_to_link(test_raw, cooked=test_HTML)
        self.assertEqual(expected_raw, result)

    # def test_test_create_topic_and_post(self):
    #     test_create_topic_and_post()
