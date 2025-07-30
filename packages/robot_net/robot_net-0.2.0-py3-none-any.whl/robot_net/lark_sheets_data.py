from urllib.parse import urlparse

import requests
from robot_base import log_decorator

from .lark_sheets import get_sheets
from .utils import get_range_name, get_range_value, get_read_range


@log_decorator
def write_sheet_data(
    access_token,
    file_url,
    sheet_name,
    range_type,
    cell,
    start_row,
    start_column,
    values,
    **kwargs,
):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [sheet for sheet in sheets if sheet.get("title") == sheet_name]
    if len(source_sheet) == 0:
        raise Exception(f"Sheet:{sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    range_name = get_range_name(
        range_type,
        source_sheet_id,
        cell,
        start_row,
        start_column,
        values,
    )
    values = get_range_value(range_type, values)
    data = {"valueRange": {"range": range_name, "values": values}}
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"写入失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def insert_sheet_data(
    access_token,
    file_url,
    sheet_name,
    range_type,
    cell,
    start_row,
    start_column,
    values,
    **kwargs,
):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [sheet for sheet in sheets if sheet.get("title") == sheet_name]
    if len(source_sheet) == 0:
        raise Exception(f"Sheet:{sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_prepend"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    range_name = get_range_name(
        range_type,
        source_sheet_id,
        cell,
        start_row,
        start_column,
        values,
    )
    values = get_range_value(range_type, values)
    data = {"valueRange": {"range": range_name, "values": values}}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"插入失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def get_sheet_data(
    access_token,
    file_url,
    sheet_name,
    range_type,
    cell,
    start_row,
    start_column,
    end_row,
    end_column,
    value_render_option,
    date_time_render_option="FormattedString",
    **kwargs,
):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [sheet for sheet in sheets if sheet.get("title") == sheet_name]
    if len(source_sheet) == 0:
        raise Exception(f"Sheet:{sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    range_name = get_read_range(
        range_type, source_sheet_id, cell, start_row, start_column, end_row, end_column
    )
    url = (
        f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range_name}?"
        + f"valueRenderOption={value_render_option}&dateTimeRenderOption={date_time_render_option}"
    )

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"获取数据失败,错误原因为:{result.get('msg')}")
        else:
            return result.get("data").get("valueRange")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")


@log_decorator
def append_sheet_data(
    access_token,
    file_url,
    sheet_name,
    range_type,
    values,
    start_row=1,
    start_column="A",
    **kwargs,
):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    spreadsheet_token = path_parts[-1]
    sheets = get_sheets(access_token, file_url)
    source_sheet = [sheet for sheet in sheets if sheet.get("title") == sheet_name]
    if len(source_sheet) == 0:
        raise Exception(f"Sheet:{sheet_name}不存在")
    source_sheet_id = source_sheet[0].get("sheet_id")
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append?insertDataOption=OVERWRITE"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token.get('tenant_access_token')}",
        "Content-Type": "application/json",
    }
    if start_row is None:
        start_row = 1
    if start_column is None:
        start_column = "A"
    range_name = get_range_name(
        range_type,
        source_sheet_id,
        "",
        start_row,
        start_column,
        values,
    )
    values = get_range_value(range_type, values)
    data = {"valueRange": {"range": f"{range_name}", "values": values}}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"添加行失败,错误原因为:{result.get('msg')}")
    else:
        raise Exception(f"网络异常,请求状态码为:{response.status_code}")
