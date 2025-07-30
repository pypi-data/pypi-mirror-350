import os
import typing
import uuid

import xlwings as xw
from robot_base import ParamException

from .utils import number_to_excel_column_number


class XlwingsExcel(object):
    app: typing.Optional[xw.App] = None

    def __init__(self):
        self.workbook: typing.Optional[xw.Book] = None

    @staticmethod
    def open_excel(
        file_path,
        is_visible,
        password=None,
        write_res_password=None,
    ) -> "XlwingsExcel":
        if XlwingsExcel.app is None:
            app = xw.App(visible=is_visible, add_book=False)
            app.display_alerts = False
            app.api.AskToUpdateLinks = False
            XlwingsExcel.app = app
        if os.path.exists(file_path):
            book = XlwingsExcel.app.books.open(
                file_path,
                update_links=False,
                password=password,
                write_res_password=write_res_password,
            )
        else:
            book = XlwingsExcel.app.books.add()
            book.save(file_path)
        excel = XlwingsExcel()
        excel.workbook = book
        return excel

    @staticmethod
    def get_opened_workbook(
        file_path,
    ) -> "XlwingsExcel":
        books = xw.books
        for book in books:
            if book.fullname == file_path:
                excel = XlwingsExcel()
                excel.workbook = book
                return excel
        else:
            raise Exception("workbook not found")

    @staticmethod
    def close_app():
        try:
            XlwingsExcel.app.quit()
            XlwingsExcel.app.kill()
        except:
            pass

    def save(self, password=None):
        self.workbook.save(password=password)

    def save_as(self, path, password=None):
        self.workbook.save(path, password=password)

    def save_as_pdf(self, path):
        self.workbook.to_pdf(path)

    def close(self):
        self.workbook.close()

    def is_sheet_exists(self, sheet_name):
        return sheet_name in [s.name for s in self.workbook.sheets]

    def get_sheet_names(self):
        return [s.name for s in self.workbook.sheets]

    def activate_sheet(self, sheet_name, sheet_index):
        if sheet_name == "" or sheet_name is None:
            self.workbook.sheets[sheet_index].select()
        elif self.is_sheet_exists(sheet_name):
            self.workbook.sheets[sheet_name].select()
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def insert_sheet(self, new_sheet_name, sheet_name, is_before):
        if self.is_sheet_exists(new_sheet_name):
            raise ParamException(
                f"{self.workbook.name} 文件中已存在 {new_sheet_name} 工作表"
            )
        if sheet_name == "" or sheet_name is None:
            sheet = self.workbook.sheets.active
        elif self.is_sheet_exists(sheet_name):
            sheet = self.workbook.sheets[sheet_name]
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )
        if is_before:
            return self.workbook.sheets.add(name=new_sheet_name, before=sheet)
        else:
            return self.workbook.sheets.add(name=new_sheet_name, after=sheet)

    def rename_sheet(self, sheet_name, new_sheet_name):
        if self.is_sheet_exists(new_sheet_name):
            raise ParamException(
                f"{self.workbook.name} 文件中已存在 {new_sheet_name} 工作表"
            )
        if self.is_sheet_exists(sheet_name):
            self.workbook.sheets[sheet_name].name = new_sheet_name
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def copy_sheet(self, sheet_name, new_sheet_name):
        if self.is_sheet_exists(new_sheet_name):
            raise ParamException(
                f"{self.workbook.name} 文件中已存在 {new_sheet_name} 工作表"
            )
        if self.is_sheet_exists(sheet_name):
            self.workbook.sheets[sheet_name].copy(name=new_sheet_name)
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def copy_sheet_to_another_workbook(
        self, sheet_name, new_sheet_name, another_workbook: "XlwingsExcel"
    ):
        if new_sheet_name in [s.name for s in another_workbook.workbook.sheets]:
            raise ParamException(
                f"{another_workbook} 文件中已存在 {new_sheet_name} 工作表"
            )
        if self.is_sheet_exists(sheet_name):
            self.workbook.sheets[sheet_name].copy(
                name=new_sheet_name, after=another_workbook.workbook.sheets.active
            )
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def delete_sheet(self, sheet_name):
        if self.is_sheet_exists(sheet_name):
            self.workbook.sheets[sheet_name].delete()
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def move_sheet_to_index(self, sheet_name, index):
        if self.is_sheet_exists(sheet_name):
            new_sheet_name = str(uuid.uuid4())[0:8]
            if index >= len(self.workbook.sheets):
                index = len(self.workbook.sheets) - 1
                self.workbook.sheets[sheet_name].copy(
                    name=new_sheet_name, after=self.workbook.sheets[index]
                )
            else:
                self.workbook.sheets[sheet_name].copy(
                    name=new_sheet_name, before=self.workbook.sheets[index]
                )
            self.workbook.sheets[sheet_name].delete()
            self.rename_sheet(new_sheet_name, sheet_name)
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def move_sheet(self, sheet_name, target_sheet_name, is_before):
        if self.is_sheet_exists(target_sheet_name):
            sheet = self.workbook.sheets[target_sheet_name]
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {target_sheet_name} 工作表"
            )
        if self.is_sheet_exists(sheet_name):
            new_sheet_name = str(uuid.uuid4())[0:8]
            if is_before:
                self.workbook.sheets[sheet_name].copy(name=new_sheet_name, before=sheet)
            else:
                self.workbook.sheets[sheet_name].copy(name=new_sheet_name, after=sheet)
            self.workbook.sheets[sheet_name].delete()
            self.rename_sheet(new_sheet_name, sheet_name)
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def get_used_range(self, sheet_name):
        if self.is_sheet_exists(sheet_name):
            used_range = self.workbook.sheets[sheet_name].used_range
            value = used_range.address.split(":")
            start_col = value[0].split("$")[1]
            start_row = value[0].split("$")[2]
            end_col = value[1].split("$")[1]
            end_row = value[1].split("$")[2]
            return start_row, start_col, end_row, end_col
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def get_row_count(self, sheet_name, by_type="sheet", column=1):
        if self.is_sheet_exists(sheet_name):
            if by_type == "sheet":
                return self.workbook.sheets[sheet_name].used_range.last_cell.row
            elif by_type == "column":
                sheet = self.workbook.sheets[sheet_name]
                return sheet.cells(sheet.cells.last_cell.row, column).end("up").row
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def get_column_count(self, sheet_name, by_type="sheet", row=1):
        if self.is_sheet_exists(sheet_name):
            if by_type == "sheet":
                return self.workbook.sheets[sheet_name].used_range.last_cell.column
            elif by_type == "row":
                sheet = self.workbook.sheets[sheet_name]
                return sheet.cells(row, sheet.cells.last_cell.column).end("left").column
        else:
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )

    def get_content(
        self,
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
    ):
        if not self.is_sheet_exists(sheet_name):
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )
        (
            used_range_start_row,
            used_range_start_col,
            used_range_end_row,
            used_range_end_col,
        ) = self.get_used_range(sheet_name)
        if range_type == "cell":
            return (
                self.workbook.sheets[sheet_name]
                .range(f"{number_to_excel_column_number(cell_column)}{cell_row}")
                .value
            )
        elif range_type == "row":
            return (
                self.workbook.sheets[sheet_name]
                .range(f"A{row}:{used_range_end_col}{row}")
                .value
            )
        elif range_type == "column":
            return (
                self.workbook.sheets[sheet_name]
                .range(
                    f"{number_to_excel_column_number(column)}1:{number_to_excel_column_number(column)}{used_range_end_row}"
                )
                .value
            )
        elif range_type == "range":
            return (
                self.workbook.sheets[sheet_name]
                .range(
                    f"{number_to_excel_column_number(start_col)}{start_row}:{number_to_excel_column_number(end_col)}{end_row}"
                )
                .value
            )
        elif range_type == "used_range":
            return self.workbook.sheets[sheet_name].used_range.value

    def write_cell(self, sheet_name, cell_column, cell_row, value):
        if not self.is_sheet_exists(sheet_name):
            raise ParamException(
                f"{self.workbook.name} 文件中不存在 {sheet_name} 工作表"
            )
        self.workbook.sheets[sheet_name].range(
            f"{number_to_excel_column_number(cell_column)}{cell_row}"
        ).value = value
