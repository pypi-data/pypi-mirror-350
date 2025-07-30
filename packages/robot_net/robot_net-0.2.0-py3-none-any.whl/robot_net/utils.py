def column_name_to_number(column_name) -> int:
    column_name = str(column_name)
    if column_name.isdigit():
        return int(column_name)
    column_number = 0
    # 将列名转换为列表，例如"AB" -> ['A', 'B']
    letters = list(column_name.upper())
    # 计算序号
    for letter in letters:
        # 将字母转换为对应的序号，例如'A' -> 1
        column_number = column_number * 26 + (ord(letter) - ord("A")) + 1
    return column_number


def number_to_excel_column_number(num):
    num = str(num)
    if not num.isdigit():
        return num
    # Excel列名的字符集大小（A-Z）
    num = int(num)
    char_set_size = 26
    # 如果数字小于26，直接返回对应的字母
    if num - 1 < char_set_size:
        return chr(num + 64)  # 将数字转换为'A'的ASCII码，然后加上当前数字
    else:
        # 否则，将数字转换为除以26的余数和商
        remainder = num % char_set_size
        quotient = num // char_set_size
        # 如果商大于26，递归调用函数处理商
        if quotient > char_set_size:
            return number_to_excel_column_number(str(quotient)) + chr(remainder + 64)
        else:
            # 如果商小于等于26，直接返回商对应的字母加上余数对应的字母
            return chr(quotient + 64) + chr(remainder + 64)


def get_range_name(range_type, sheet_id, cell, start_row, start_column, values):
    range_name = f"{sheet_id}"
    if range_type == "cell":
        range_name += f"!{cell}:{cell}"
    elif range_type == "row":
        start_col_name = number_to_excel_column_number(start_column)
        start_col = column_name_to_number(start_column)
        end_col_name = number_to_excel_column_number(start_col + len(values) - 1)
        range_name += f"!{start_col_name}{start_row}:{end_col_name}{start_row}"
    elif range_type == "col":
        start_col_name = number_to_excel_column_number(start_column)
        range_name += (
            f"!{start_col_name}{start_row}:{start_col_name}{int(start_row)+len(values)}"
        )
    elif range_type == "range":
        start_col_name = number_to_excel_column_number(start_column)
        start_col = column_name_to_number(start_column)
        end_row = int(start_row) + len(values) - 1
        end_col = max([len(values[i]) for i in range(len(values))]) + start_col
        end_col_name = number_to_excel_column_number(end_col)
        range_name += f"!{start_col_name}{start_row}:{end_col_name}{end_row}"
    else:
        pass
    return range_name


def get_read_range(
    range_type, sheet_id, cell, start_row, start_column, end_row, end_column
):
    range_name = f"{sheet_id}"
    if range_type == "cell":
        range_name += f"!{cell}:{cell}"
    elif range_type == "row":
        end_col_name = number_to_excel_column_number(end_column)
        range_name += f"!A{start_row}:{end_col_name}{end_row}"
    elif range_type == "col":
        start_col_name = number_to_excel_column_number(start_column)
        end_col_name = number_to_excel_column_number(end_column)
        range_name += f"!{start_col_name}{0}:{end_col_name}"
    elif range_type == "range":
        start_col_name = number_to_excel_column_number(start_column)
        end_col_name = number_to_excel_column_number(end_column)
        range_name += f"!{start_col_name}{start_row}:{end_col_name}{end_row}"
    else:
        pass
    return range_name


def get_range_value(range_type, values):
    if range_type == "cell":
        return [[values]]
    elif range_type == "row":
        return [values]
    elif range_type == "col":
        return [[value] for value in values]
    elif range_type == "range":
        return values
    return values
