from openpyxl import Workbook, load_workbook
import os


class ExcelManager:

    def __init__(self, filename="voucher.xlsx"):
        self.filename = filename

    def create_file(self):

        if not os.path.exists(self.filename):

            wb = Workbook()

            ws = wb.active

            ws.title = "Voucher"

            ws.append([
                "Name",
                "Voucher No",
                "Amount",
                "Date",
                "Time"
            ])

            wb.save(self.filename)

    def save_data(self,
                  name,
                  voucher,
                  amount,
                  date,
                  time):

        self.create_file()

        wb = load_workbook(self.filename)

        ws = wb.active

        ws.append([
            name,
            voucher,
            amount,
            date,
            time
        ])

        wb.save(self.filename)

    def total_rows(self):

        if not os.path.exists(self.filename):
            return 0

        wb = load_workbook(self.filename)

        ws = wb.active

        return ws.max_row - 1
