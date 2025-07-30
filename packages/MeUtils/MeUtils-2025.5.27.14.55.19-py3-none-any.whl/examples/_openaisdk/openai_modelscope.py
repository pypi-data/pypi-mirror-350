#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
Qwen/Qwen2.5-Coder-32B-InstructQwen/Qwen2.5-Coder-14B-InstructQwen/Qwen2.5-Coder-7B-InstructQwen/Qwen2.5-72B-InstructQwen/Qwen2.5-32B-InstructQwen/Qwen2.5-14B-InstructQwen/Qwen2.5-7B-Instruct

Qwen/QVQ-72B-Preview
"""
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError

client = OpenAI(
    # api_key=os.getenv("STEP_API_KEY"),
    # base_url="https://api.stepfun.com/v1",
    base_url=os.getenv("MODELSCOPE_BASE_URL"),
    # api_key=os.getenv("MODELSCOPE_API_KEY"),
    api_key="411524c8-1507-440c-8a67-874fc29e700e"
)

print(client.models.list())

try:
    completion = client.chat.completions.create(
        # model="step-1-8k",
        # model="Qwen/QwQ-32B-Preview",
        # model="Qwen/QVQ-72B-Preview",
        # model="qwen/qvq-72b-preview",

        messages=[
            {"role": "user", "content": "你是谁"}
        ],
        # top_p=0.7,
        top_p=None,
        temperature=None,
        stream=True,
        max_tokens=1000
    )
except APIStatusError as e:
    print(e.status_code)

    print(e.response)
    print(e.message)
    print(e.code)

for chunk in completion:
    print(chunk.choices[0].delta.content)
