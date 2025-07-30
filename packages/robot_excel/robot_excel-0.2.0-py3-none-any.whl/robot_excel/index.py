import os

import robot_base

from .utils import column_name_to_number
from .xlwings_excel import XlwingsExcel


@robot_base.log_decorator
@robot_base.func_decorator
def open_excel(
    file_path,
    open_type,
    is_visible=False,
    create_new=True,
    password=None,
    write_res_password=None,
    **kwargs,
):
    if not os.path.exists(file_path) and not create_new:
        raise robot_base.ParamException(f"{file_path}文件不存在")
    if open_type == "xlwings":
        excel_app = XlwingsExcel.open_excel(
            file_path,
            is_visible=is_visible,
            password=password,
            write_res_password=write_res_password,
        )
        return excel_app
    else:
        raise robot_base.ParamException(f"不支持的open_type:{open_type}")


@robot_base.log_decorator
@robot_base.func_decorator
def get_opened_workbook(
    file_path,
    **kwargs,
):
    excel_app = XlwingsExcel.get_opened_workbook(file_path)
    return excel_app


@robot_base.log_decorator
@robot_base.func_decorator
def close_excel(
    excel_app: XlwingsExcel,
    is_save,
    close_all,
    **kwargs,
):
    if is_save:
        excel_app.save()
    if close_all:
        excel_app.close_app()
    else:
        excel_app.close()


@robot_base.log_decorator
@robot_base.func_decorator
def save_workbook(
    excel_app: XlwingsExcel,
    **kwargs,
):
    excel_app.save()


@robot_base.log_decorator
@robot_base.func_decorator
def save_workbook_as(
    excel_app: XlwingsExcel,
    path,
    **kwargs,
):
    excel_app.save_as(path)


@robot_base.log_decorator
@robot_base.func_decorator
def encrypt_workbook(
    excel_app: XlwingsExcel,
    file_path,
    password,
    **kwargs,
):
    excel_app.save_as(file_path, password=password)


@robot_base.log_decorator
@robot_base.func_decorator
def save_workbook_as_pdf(
    excel_app: XlwingsExcel,
    path,
    **kwargs,
):
    excel_app.save_as_pdf(path)


@robot_base.log_decorator
@robot_base.func_decorator
def get_sheet_names(
    excel_app: XlwingsExcel,
    **kwargs,
):
    return excel_app.get_sheet_names()


@robot_base.log_decorator
@robot_base.func_decorator
def activate_sheet(
    excel_app: XlwingsExcel,
    active_type,
    sheet_name,
    sheet_index,
    **kwargs,
):
    if sheet_index is not None:
        sheet_index = int(sheet_index)
    if active_type == "name":
        if sheet_name == "" or sheet_name is None:
            raise robot_base.ParamException("sheet_name不能为空")
        excel_app.activate_sheet(sheet_name, sheet_index)
    else:
        excel_app.activate_sheet("", sheet_index)


@robot_base.log_decorator
@robot_base.func_decorator
def insert_sheet(
    excel_app: XlwingsExcel,
    sheet_name,
    new_sheet_name,
    is_before,
    **kwargs,
):
    return excel_app.insert_sheet(
        new_sheet_name=new_sheet_name, sheet_name=sheet_name, is_before=is_before
    )


@robot_base.log_decorator
@robot_base.func_decorator
def rename_sheet(
    excel_app: XlwingsExcel,
    sheet_name,
    new_sheet_name,
    **kwargs,
):
    excel_app.rename_sheet(sheet_name=sheet_name, new_sheet_name=new_sheet_name)


@robot_base.log_decorator
@robot_base.func_decorator
def copy_sheet(
    excel_app: XlwingsExcel,
    sheet_name,
    target_type,
    another_workbook: "XlwingsExcel",
    new_sheet_name,
    **kwargs,
):
    if target_type == "another_workbook":
        if another_workbook is None:
            raise robot_base.ParamException("another_workbook不能为空")
        excel_app.copy_sheet_to_another_workbook(
            sheet_name=sheet_name,
            new_sheet_name=new_sheet_name,
            another_workbook=another_workbook,
        )
    else:
        excel_app.copy_sheet(sheet_name=sheet_name, new_sheet_name=new_sheet_name)


@robot_base.log_decorator
@robot_base.func_decorator
def delete_sheet(
    excel_app: XlwingsExcel,
    sheet_name,
    **kwargs,
):
    excel_app.delete_sheet(sheet_name=sheet_name)


@robot_base.log_decorator
@robot_base.func_decorator
def move_sheet(
    excel_app: XlwingsExcel,
    sheet_name,
    target_type,
    target_sheet_name,
    is_before,
    index,
    **kwargs,
):
    if target_type == "index":
        index = int(index)
        excel_app.move_sheet_to_index(sheet_name=sheet_name, index=index)
    else:
        excel_app.move_sheet(
            sheet_name=sheet_name,
            target_sheet_name=target_sheet_name,
            is_before=is_before,
        )


@robot_base.log_decorator
@robot_base.func_decorator
def get_used_range(
    excel_app: XlwingsExcel,
    sheet_name,
    **kwargs,
):
    return excel_app.get_used_range(sheet_name=sheet_name)


@robot_base.log_decorator
@robot_base.func_decorator
def get_row_count(
    excel_app: XlwingsExcel,
    sheet_name,
    by_type,
    column,
    **kwargs,
):
    return excel_app.get_row_count(
        sheet_name=sheet_name,
        by_type=by_type,
        column=column_name_to_number(column),
    )


@robot_base.log_decorator
@robot_base.func_decorator
def get_column_count(
    excel_app: XlwingsExcel,
    sheet_name,
    by_type,
    row,
    **kwargs,
):
    if row is not None:
        row = int(row)
    return excel_app.get_column_count(
        sheet_name=sheet_name,
        by_type=by_type,
        row=row,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def get_content(
    excel_app: XlwingsExcel,
    sheet_name,
    range_type,
    cell_column="A",
    cell_row=1,
    row=1,
    column="A",
    start_row=1,
    start_col="A",
    end_row=1,
    end_col="B",
    **kwargs,
):
    if cell_row is not None:
        cell_row = int(cell_row)
    if row is not None:
        row = int(row)
    if start_row is not None:
        row = int(start_row)
    if end_row is not None:
        row = int(end_row)
    return excel_app.get_content(
        sheet_name=sheet_name,
        range_type=range_type,
        cell_column=cell_column,
        cell_row=cell_row,
        row=row,
        column=column,
        start_row=start_row,
        start_col=start_col,
        end_row=end_row,
        end_col=end_col,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def write_cell(
    excel_app: XlwingsExcel,
    sheet_name,
    cell_column,
    cell_row,
    value,
    **kwargs,
):
    cell_row = int(cell_row)
    return excel_app.write_cell(
        sheet_name=sheet_name, cell_column=cell_column, cell_row=cell_row, value=value
    )
