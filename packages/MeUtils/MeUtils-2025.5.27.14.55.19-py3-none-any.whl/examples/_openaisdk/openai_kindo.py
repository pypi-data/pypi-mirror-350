#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError


client = OpenAI(
    # base_url="https://free.chatfire.cn/v1",
    api_key="9a867a14-26d1-4950-89ae-dd989dec10b5-b137b199a507d6f5",
    base_url="https://all.chatfire.cc/kindo/v1"

)

try:
    client.chat.completions.create(
        messages=[
            {"role": "user", "content": "你是谁"}
        ],
        model="azure/gpt-4o-mini",
    )
except Exception as e:
    print(e)