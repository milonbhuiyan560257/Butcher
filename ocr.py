"""
OCR Module - Android compatible version
"""

import os


class OCRReader:

    def __init__(self):
        pass

    def extract_text(self, image_path):
        if not os.path.exists(image_path):
            return ""

        return self._demo_text()

    def _demo_text(self):
        return """Name: Rahim Uddin
Voucher: V-10258
Amount: 1500
Date: 01/08/2026
Mobile: 01712345678"""

    def process_image(self, image_path):
        from parser import VoucherParser

        text = self.extract_text(image_path)
        if not text:
            return None

        parser = VoucherParser()
        return parser.parse(text)
