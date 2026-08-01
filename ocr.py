import re

class OCRReader:

    def __init__(self):
        pass

    def process_text(self, text):

        result = {
            "name": "",
            "voucher": "",
            "amount": ""
        }

        for line in text.splitlines():

            line = line.strip()

            if line.lower().startswith("name"):
                result["name"] = line.split(":", 1)[-1].strip()

            elif "voucher" in line.lower():
                result["voucher"] = line.split(":", 1)[-1].strip()

            elif "amount" in line.lower():
                result["amount"] = re.sub(r"[^0-9.]", "", line)

        return result
