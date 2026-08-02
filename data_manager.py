"""
Data Manager - Uses CSV (pure Python, works on Android)
CSV can be opened in Excel, Google Sheets, etc.
"""

import csv
import os


class DataManager:

    def __init__(self, filename="voucher_data.csv"):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Voucher No", "Amount", "Mobile", "Date", "Time"])

    def save_data(self, name, voucher, amount, mobile, date, time):
        self._ensure_file()
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, voucher, amount, mobile, date, time])

    def total_rows(self):
        if not os.path.exists(self.filename):
            return 0
        with open(self.filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            return sum(1 for _ in reader)

    def get_all_data(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            return list(reader)
