import base64
import hashlib
import hmac
import json
import os.path
import pathlib
import time

import requests
from requests_toolbelt import MultipartEncoder
from robot_base import log_decorator


@log_decorator
def send_webhook_message(
    webhook_url,
    message_type,
    message_content,
    at_type,
    at_user_id,
    at_username,
    is_sign,
    secret,
    **kwargs,
):

    if message_type == "text":
        at_content = ""
        if at_type == "all":
            at_content = f"<at user_id=all>所有人</at>"
        elif at_type == "user":
            at_content = f"<at user_id={at_user_id}>{at_username}</at>"
        req = {
            "msg_type": "text",
            "content": {"text": f"{at_content} {message_content}"},
        }
    elif message_type == "post":
        req = {
            "msg_type": "post",
            "content": {"post": message_content},
        }
    else:
        req = {
            "msg_type": "interactive",
            "card": message_content,
        }
    if is_sign:
        timestamp = int(time.time())
        sign = gen_sign(timestamp, secret)
        req["timestamp"] = timestamp
        req["sign"] = sign
    response = requests.post(webhook_url, json=req)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容
        token_info = response.json()
        # 检查是否成功获取token
        if token_info.get("code") != 0:
            raise Exception(f"获取飞书凭证失败:{token_info.get('msg')}")
    else:
        raise Exception(f"获取飞书凭证失败,请求状态码为:{response.status_code}")


def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = "{}\n{}".format(timestamp, secret)
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


@log_decorator
def send_text_message(
    access_token,
    receive_id_type,
    receive_id,
    message_content,
    at_type,
    at_user_id,
    at_username,
    **kwargs,
):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": receive_id_type}
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    at_content = ""
    if at_type == "all":
        at_content = f'<at user_id="all">所有人</at>'
    elif at_type == "user":
        at_content = f'<at user_id="{at_user_id}">{at_username}</at>'
    msg_content = {
        "text": at_content + " " + message_content,
    }
    req = {
        "receive_id": receive_id,  # chat id
        "msg_type": "text",
        "content": json.dumps(msg_content),
    }
    payload = json.dumps(req)
    response = requests.request(
        "POST", url, params=params, headers=headers, data=payload
    )
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"发送消息失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def send_file_message(
    access_token,
    receive_id_type,
    receive_id,
    file_type,
    file_path,
    **kwargs,
):
    if not os.path.exists((file_path)):
        raise Exception(f"文件不存在:{file_path}")

    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": receive_id_type}
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    if file_type == "image":
        image_key = send_image_to_server(access_token, file_path)
        msg_content = {"image_key": image_key}
    else:
        file_key = send_file_to_server(access_token, file_path)
        msg_content = {"file_key": file_key}
    req = {
        "receive_id": receive_id,  # chat id
        "msg_type": file_type,
        "content": json.dumps(msg_content),
    }
    payload = json.dumps(req)
    response = requests.request(
        "POST", url, params=params, headers=headers, data=payload
    )
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"发送消息失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


def send_image_to_server(
    access_token,
    image_path,
    **kwargs,
):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {
        "image_type": "message",
        "image": (open(image_path, "rb")),
    }  # 需要替换具体的path
    multi_form = MultipartEncoder(form)
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
    }
    headers["Content-Type"] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"上传图片失败,错误原因为:{result.get('msg')}")
        return result.get("data").get("image_key")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


def send_file_to_server(access_token, file_path, **kwargs):
    file_path = pathlib.Path(file_path)
    file_type = "stream"
    if file_path.suffix == ".doc" or file_path.suffix == ".docx":
        file_type = "doc"
    elif file_path.suffix == ".xls" or file_path.suffix == ".xlsx":
        file_type = "xls"
    elif file_path.suffix == ".ppt" or file_path.suffix == ".pptx":
        file_type = "ppt"
    elif file_path.suffix == ".pdf":
        file_type = "pdf"
    elif file_path.suffix == ".mp4":
        file_type = "mp4"
    elif file_path.suffix == ".opus":
        file_type = "opus"
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    form = {
        "file_type": file_type,
        "file_name": file_path.name,
        "file": (file_path.name, open(file_path, "rb"), "text/plain"),
    }
    multi_form = MultipartEncoder(form)
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
    }
    headers["Content-Type"] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"上传图片失败,错误原因为:{result.get('msg')}")
        return result.get("data").get("file_key")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")
