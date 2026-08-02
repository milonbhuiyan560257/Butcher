"""
OCR Module - Tesseract ব্যবহার করে ছবি থেকে টেক্সট বের করে।
Android-এর জন্য buildozer.spec-এ tesseract যোগ করতে হবে।
"""

import os
from PIL import Image, ImageEnhance, ImageFilter

# Tesseract import with fallback
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


class OCRReader:

    def __init__(self, lang="eng+ben"):
        self.lang = lang
        
    def _preprocess_image(self, image_path):
        """
        ছবির কোয়ালিটি বাড়ানোর জন্য প্রি-প্রসেসিং:
        - Grayscale
        - Contrast বাড়ানো
        - Noise কমানো (thresholding)
        """
        img = Image.open(image_path)
        
        # RGBA → RGB (যদি প্রয়োজন হয়)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Grayscale
        img = img.convert('L')
        
        # Contrast enhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # Sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        
        # Thresholding (Otsu-like simple threshold)
        img = img.point(lambda x: 0 if x < 128 else 255, '1')
        img = img.convert('L')
        
        return img

    def extract_text(self, image_path):
        """
        ছবি থেকে সম্পূর্ণ টেক্সট বের করে।
        Tesseract না থাকলে demo টেক্সট ফেরত দেয়।
        """
        if not os.path.exists(image_path):
            return ""

        if not TESSERACT_AVAILABLE:
            # Demo mode - Tesseract ইনস্টল না থাকলে
            return self._demo_text()

        try:
            processed = self._preprocess_image(image_path)
            
            # Tesseract OCR
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(
                processed,
                lang=self.lang,
                config=custom_config
            )
            
            return text.strip()
        except Exception as e:
            print(f"OCR Error: {e}")
            return self._demo_text()

    def _demo_text(self):
        """ডেভেলপমেন্ট/টেস্টিং এর জন্য ডেমো ডাটা"""
        return """
Name: Rahim Uddin
Voucher: V-10258
Amount: 1500
Date: 01/08/2026
Mobile: 01712345678
"""

    def process_image(self, image_path):
        """
        ছবি → টেক্সট → Dictionary
        """
        from parser import VoucherParser
        
        text = self.extract_text(image_path)
        if not text:
            return None
        
        parser = VoucherParser()
        return parser.parse(text)
