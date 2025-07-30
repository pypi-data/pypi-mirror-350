from urllib.parse import urlparse, parse_qs

import requests
from robot_base import log_decorator


@log_decorator
def get_bit_sheet_data(access_token, file_url, page_token, **kwargs):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    app_token = path_parts[-1]
    query_params = parse_qs(parsed_url.query)
    table_id = query_params["table"][0]
    view_id = query_params["view"][0]
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search?page_size=500&user_id_type=open_id"
    if page_token:
        url += f"&page_token={page_token}"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    data = {"view_id": view_id}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"获取多维表格数据失败,错误原因为:{result.get('msg')}")
        else:
            return result.get("data")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def delete_bit_sheet_record(access_token, file_url, record_id, **kwargs):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    app_token = path_parts[-1]
    query_params = parse_qs(parsed_url.query)
    table_id = query_params["table"][0]
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"删除多维表格数据失败,错误原因为:{result.get('msg')}")
        else:
            return result.get("data")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")
