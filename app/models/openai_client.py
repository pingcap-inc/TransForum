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

import openai
from app.config import conf
from app.models import system_content_msg, system_title_msg
from retrying import retry
import langid

model_name = "gpt-4o"
open_ai_client = openai.OpenAI(
    api_key=conf.open_ai_api,
    base_url=conf.open_ai_base_url,
)

max_length_of_title = 255
long_text_thresholds = 2000
long_text_window_size = 2
langid.set_languages(['zh', 'en'])


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def request_openai(messages):
    response = open_ai_client.chat.completions.create(
        model=model_name,
        temperature=0.1,
        messages=messages)
    result = response.choices[0].message.content
    lang, _ = langid.classify(result)

    # Use NLP to check if it's a Chinese content to ensure the translation quality
    if lang == 'zh':
        new_message = messages + [
            {"role": "assistant", "content": result},
            {"role": "user", "content": "You are wrong! We need English content, "
                                        "directly translate it, don't say anything else."}]

        response = open_ai_client.chat.completions.create(
            model=model_name,
            temperature=0.1,
            messages=new_message)

        # Still Chinese? I don't know how to deal with that.... Just return.
        result = response.choices[0].message.content

    # Return the translated context
    return result


def translate_title(text):
    messages = [{"role": "system", "content": system_title_msg},
                {"role": "user", "content": text}]
    response = request_openai(messages=messages)

    if len(response) > max_length_of_title:
        messages = messages + [
            {"role": "assistant", "content": response},
            {"role": "user", "content": "It's too long to save as a title, please check the length. "
                                        "We need to shorten it to less than 255 characters"}
        ]

        response = request_openai(messages=messages)
        # if still exceed... just cut it.
        response = response[:max_length_of_title]

    return response


def translate(text):
    return request_openai(messages=[{"role": "system", "content": system_content_msg},
                                    {"role": "user", "content": text}])
