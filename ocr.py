# ocr.py

import os
from parser import VoucherParser


class OCRReader:

    def __init__(self):
        self.parser = VoucherParser()

    def extract_text(self, image_path):
        """
        এখানে ভবিষ্যতে OCR Engine (ML Kit / Tesseract / অন্য কিছু)
        থেকে টেক্সট নেওয়া হবে।

        বর্তমানে এটি ডেমো হিসেবে একটি নমুনা টেক্সট ফেরত দিচ্ছে।
        """

        if not os.path.exists(image_path):
            return ""

        demo_text = """
        Name: Rahim Uddin
        Voucher: V-10258
        Amount: 1500
        Date: 01/08/2026
        Mobile: 01712345678
        """

        return demo_text

    def process_image(self, image_path):
        """
        ছবি → টেক্সট → parser.py → Dictionary
        """

        text = self.extract_text(image_path)

        if not text:
            return None

        data = self.parser.parse(text)

        return data
