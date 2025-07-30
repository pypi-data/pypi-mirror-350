import base64
import os
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from robot_base import func_decorator, log_decorator, ParamException


@log_decorator
@func_decorator
def request_ai(
    base_url,
    api_key,
    model,
    system_prompt,
    user_prompt,
    temperature=0.1,
    is_stream=False,
    **kwargs,
):
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages: List[ChatCompletionMessageParam] = []
    if system_prompt is not None and system_prompt != "":
        messages.append({"role": "system", "content": system_prompt})

    if user_prompt is not None and user_prompt != "":
        messages.append({"role": "user", "content": user_prompt})
    else:
        raise ParamException("用户输入不能为空")
    temperature = float(temperature) if temperature is not None else 0.1
    if is_stream:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
        return content
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message.content


@log_decorator
@func_decorator
def request_ai_vl(
    base_url,
    api_key,
    model,
    system_prompt,
    user_prompt,
    file_path,
    temperature=0.1,
    is_stream=False,
    **kwargs,
):
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages: List[ChatCompletionMessageParam] = []
    if system_prompt is not None and system_prompt != "":
        messages.append({"role": "system", "content": system_prompt})

    if user_prompt is None or user_prompt == "":
        raise ParamException("用户输入不能为空")
    # 判断图片是否存在
    if not file_path:
        raise ParamException("图片路径不能为空")
    if not os.path.exists(file_path):
        raise ParamException("图片不存在")
    with open(file_path, "rb") as img_file:
        img_base = base64.b64encode(img_file.read()).decode("utf-8")
    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": img_base}},
                {"type": "text", "text": user_prompt},
            ],
        }
    )
    temperature = float(temperature) if temperature is not None else 0.1
    if is_stream:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
        return content
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message.content
