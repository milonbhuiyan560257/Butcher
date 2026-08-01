import re


class VoucherParser:

    def __init__(self):
        pass

    def parse(self, text):

        data = {
            "name": "",
            "voucher": "",
            "amount": "",
            "date": "",
            "mobile": ""
        }

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            low = line.lower()

            # Name
            if low.startswith("name"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    data["name"] = parts[1].strip()

            # Voucher
            elif "voucher" in low:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    data["voucher"] = parts[1].strip()

            # Amount
            elif "amount" in low or "total" in low:
                m = re.search(r"([0-9]+(?:\.[0-9]+)?)", line)
                if m:
                    data["amount"] = m.group(1)

            # Date
            elif "date" in low:
                m = re.search(
                    r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
                    line
                )
                if m:
                    data["date"] = m.group(1)

            # Mobile
            m = re.search(r"(01[3-9]\d{8})", line)
            if m:
                data["mobile"] = m.group(1)

        return data
