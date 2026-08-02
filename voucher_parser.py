"""
Smart Voucher Parser
"""

import re


class VoucherParser:

    def __init__(self):
        self.patterns = {
            "voucher": [
                r'[Vv]oucher[\s:#-]*([A-Za-z0-9\-]+)',
                r'[Vv]oucher\s*[Nn]o[\s:.#-]*([A-Za-z0-9\-]+)',
                r'[Bb]ill[\s:#-]*([A-Za-z0-9\-]+)',
                r'[Rr]eceipt[\s:#-]*([A-Za-z0-9\-]+)',
                r'[Nn]o[\s:.#-]*([A-Z]{1,3}-?\d{3,8})',
                r'^(V-?\d{3,8})$',
                r'^(INV-?\d{3,8})$',
            ],
            "amount": [
                r'[Aa]mount[\s:]*([0-9,]+(?:\.[0-9]{1,2})?)',
                r'[Tt]otal[\s:]*([0-9,]+(?:\.[0-9]{1,2})?)',
                r'[Tt]aka[\s:]*([0-9,]+(?:\.[0-9]{1,2})?)',
                r'[Bb]ill[\s:]*([0-9,]+(?:\.[0-9]{1,2})?)',
                r'\b([0-9,]+(?:\.[0-9]{1,2})?)\s*(?:TK|Tk|tk|BDT|৳)',
                r'[Pp]rice[\s:]*([0-9,]+(?:\.[0-9]{1,2})?)',
                r'[Ff]ee[\s:]*([0-9,]+(?:\.[0-9]{1,2})?)',
                r'\b(?:TK|Tk|tk|BDT|৳)\s*([0-9,]+(?:\.[0-9]{1,2})?)',
            ],
            "date": [
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{2,4}[/-]\d{1,2}[/-]\d{1,2})',
            ],
            "mobile": [
                r'(01[3-9]\d{8})',
                r'(?:\+88)?\s*(01[3-9]\d{8})',
                r'(8801[3-9]\d{8})',
            ],
            "name": [
                r'[Nn]ame[\s:]*([A-Za-z\s\.]+?)(?=[A-Z][a-z]+[\s:]|$)',
                r'[Cc]ustomer[\s:]*([A-Za-z\s\.]+?)(?=[A-Z][a-z]+[\s:]|$)',
                r'[Pp]atient[\s:]*([A-Za-z\s\.]+?)(?=[A-Z][a-z]+[\s:]|$)',
            ]
        }

    def parse(self, text):
        data = {"name": "", "voucher": "", "amount": "", "date": "", "mobile": ""}
        lines = text.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            low = line.lower()

            if any(k in low for k in ["name", "customer", "patient", "নাম"]):
                parts = re.split(r'[:\-#=]', line, maxsplit=1)
                if len(parts) == 2:
                    name = parts[1].strip()
                    name = re.sub(r'\b(voucher|amount|date|mobile|total|bill)\b.*$', '', name, flags=re.I).strip()
                    if len(name) > 2:
                        data["name"] = name

            elif any(k in low for k in ["voucher", "bill", "receipt", "invoice", "no", "ভাউচার"]):
                for pattern in self.patterns["voucher"]:
                    m = re.search(pattern, line, re.I)
                    if m:
                        data["voucher"] = m.group(1).strip()
                        break

            elif any(k in low for k in ["amount", "total", "taka", "price", "fee", "টাকা", "মোট"]):
                for pattern in self.patterns["amount"]:
                    m = re.search(pattern, line, re.I)
                    if m:
                        data["amount"] = m.group(1).replace(',', '')
                        break

            elif any(k in low for k in ["date", "তারিখ"]):
                for pattern in self.patterns["date"]:
                    m = re.search(pattern, line)
                    if m:
                        data["date"] = m.group(1)
                        break

            for pattern in self.patterns["mobile"]:
                m = re.search(pattern, line)
                if m:
                    mobile = m.group(1)
                    if mobile.startswith('88'):
                        mobile = mobile[2:]
                    data["mobile"] = mobile
                    break

        if not data["voucher"]:
            for pattern in self.patterns["voucher"]:
                m = re.search(pattern, text, re.I | re.M)
                if m:
                    data["voucher"] = m.group(1).strip()
                    break

        if not data["amount"]:
            for pattern in self.patterns["amount"]:
                m = re.search(pattern, text, re.I | re.M)
                if m:
                    data["amount"] = m.group(1).replace(',', '')
                    break

        if not data["date"]:
            for pattern in self.patterns["date"]:
                m = re.search(pattern, text, re.I | re.M)
                if m:
                    data["date"] = m.group(1)
                    break

        if not data["mobile"]:
            for pattern in self.patterns["mobile"]:
                m = re.search(pattern, text)
                if m:
                    mobile = m.group(1)
                    if mobile.startswith('88'):
                        mobile = mobile[2:]
                    data["mobile"] = mobile
                    break

        if not data["name"]:
            m = re.search(r'[Nn]ame[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text)
            if m:
                data["name"] = m.group(1).strip()

        if data["amount"]:
            data["amount"] = re.sub(r'[^0-9.]', '', data["amount"])
            parts = data["amount"].split('.')
            if len(parts) > 2:
                data["amount"] = parts[0] + '.' + ''.join(parts[1:])

        return data
