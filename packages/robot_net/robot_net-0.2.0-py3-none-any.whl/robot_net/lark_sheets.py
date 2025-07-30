from urllib.parse import urlparse

import requests
from robot_base import log_decorator


@log_decorator
def get_sheets(access_token, file_url, **kwargs):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"复制Sheet失败,错误原因为:{result.get('msg')}")
        else:
            return result.get("data").get("sheets")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def add_sheet(access_token, file_url, sheet_name, index=0, **kwargs):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    index = int(index)
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    data = {
        "requests": [
            {"addSheet": {"properties": {"title": sheet_name, "index": index}}}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"添加Sheet失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def copy_sheet(access_token, file_url, source_sheet_name, target_sheet_name, **kwargs):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [
        sheet for sheet in sheets if sheet.get("title") == source_sheet_name
    ]
    if len(source_sheet) == 0:
        raise Exception(f"源Sheet{source_sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    data = {
        "requests": [
            {
                "copySheet": {
                    "source": {"sheetId": source_sheet_id},
                    "destination": {"title": target_sheet_name},
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"复制Sheet失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def delete_sheet(access_token, file_url, sheet_name, **kwargs):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [sheet for sheet in sheets if sheet.get("title") == sheet_name]
    if len(source_sheet) == 0:
        raise Exception(f"Sheet:{sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    data = {"requests": [{"deleteSheet": {"sheetId": source_sheet_id}}]}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"删除Sheet失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def update_sheet(
    access_token, file_url, sheet_name, new_sheet_name, index, is_hide, **kwargs
):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [sheet for sheet in sheets if sheet.get("title") == sheet_name]
    if len(source_sheet) == 0:
        raise Exception(f"Sheet:{sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    if index:
        index = int(index)
    data = {
        "requests": [
            {
                "updateSheet": {
                    "properties": {
                        "sheetId": source_sheet_id,
                        "title": new_sheet_name,
                        "index": index,
                        "hidden": is_hide,
                    }
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"删除Sheet失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def get_sheet(access_token, file_url, sheet_name, **kwargs):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [sheet for sheet in sheets if sheet.get("title") == sheet_name]
    if len(source_sheet) == 0:
        raise Exception(f"Sheet:{sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{source_sheet_id}"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"获取Sheet信息失败,错误原因为:{result.get('msg')}")
        else:
            return result.get("data").get("sheet")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")
