import requests
from robot_base import log_decorator


@log_decorator
def get_app_access_token(app_id, app_secret, **kwargs):
    # 获取app_access_token的API URL
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"

    # 构造请求数据
    data = {"app_id": app_id, "app_secret": app_secret}

    # 发起POST请求
    response = requests.post(url, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容
        token_info = response.json()
        # 检查是否成功获取token
        if token_info.get("code") == 0:
            # 获取app_access_token
            token_info["app_id"] = app_id
            token_info["app_secret"] = app_secret
            return token_info
        else:
            raise Exception(f"获取飞书凭证失败:{token_info.get('msg')}")
    else:
        raise Exception(f"获取飞书凭证失败,请求状态码为:{response.status_code}")
