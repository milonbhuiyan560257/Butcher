from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window

from camera import CameraManager
from excel import ExcelManager
from ocr import OCRReader
from parser import VoucherParser

from datetime import datetime
import os


class VoucherScanner(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=5, **kwargs)
        
        Window.softinput_mode = "below_target"

        self.excel = ExcelManager()
        self.ocr = OCRReader()
        self.parser = VoucherParser()
        self.camera_mgr = CameraManager()

        # ── Camera ──
        self.camera = self.camera_mgr.get_widget()
        self.camera.size_hint = (1, 0.45)
        self.add_widget(self.camera)

        # ── Status ──
        self.status = Label(
            text="প্রস্তুত | Ready",
            size_hint=(1, 0.06),
            color=(0.2, 0.6, 1, 1),
            bold=True
        )
        self.add_widget(self.status)

        # ── Input Fields ──
        self.name = TextInput(
            hint_text="শিশুর নাম / Child Name",
            multiline=False,
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.name)

        self.voucher = TextInput(
            hint_text="ভাউচার নম্বর / Voucher Number",
            multiline=False,
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.voucher)

        self.amount = TextInput(
            hint_text="টাকার পরিমাণ / Amount",
            multiline=False,
            input_filter="float",
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.amount)

        self.mobile = TextInput(
            hint_text="মোবাইল নম্বর / Mobile",
            multiline=False,
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.mobile)

        # ── Buttons ──
        btn_grid = GridLayout(cols=2, size_hint=(1, 0.14), spacing=5)
        
        btn_capture = Button(
            text="📷 ছবি তুলুন",
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        btn_capture.bind(on_press=self.capture)
        btn_grid.add_widget(btn_capture)

        btn_ocr = Button(
            text="🔍 OCR চালু করুন",
            background_color=(0.9, 0.5, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        btn_ocr.bind(on_press=self.run_ocr)
        btn_grid.add_widget(btn_ocr)

        btn_save = Button(
            text="💾 Excel-এ সেভ করুন",
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        btn_save.bind(on_press=self.save_excel)
        btn_grid.add_widget(btn_save)

        btn_clear = Button(
            text="🗑️ ফিল্ড খালি করুন",
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        btn_clear.bind(on_press=self.clear_fields)
        btn_grid.add_widget(btn_clear)

        self.add_widget(btn_grid)

        # ── Recent Entries Label ──
        self.entries_label = Label(
            text="সাম্প্রতিক এন্ট্রি: ০টি",
            size_hint=(1, 0.05),
            color=(0.4, 0.4, 0.4, 1)
        )
        self.add_widget(self.entries_label)
        
        self.update_entry_count()

    def capture(self, instance):
        os.makedirs("captures", exist_ok=True)
        filename = self.camera_mgr.capture(folder="captures")
        self.status.text = f"ছবি সেভ হয়েছে: {os.path.basename(filename)}"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "প্রস্তুত | Ready"), 3)

    def run_ocr(self, instance):
        latest_img = self.camera_mgr.get_latest_capture()
        if not latest_img or not os.path.exists(latest_img):
            self.status.text = "❌ আগে ছবি তুলুন!"
            return

        self.status.text = "🔍 OCR চলছে..."
        
        def do_ocr(dt):
            try:
                text = self.ocr.extract_text(latest_img)
                if not text:
                    self.status.text = "❌ কোনো টেক্সট পাওয়া যায়নি"
                    return

                data = self.parser.parse(text)
                
                if data.get("name"):
                    self.name.text = data["name"]
                if data.get("voucher"):
                    self.voucher.text = data["voucher"]
                if data.get("amount"):
                    self.amount.text = data["amount"]
                if data.get("mobile"):
                    self.mobile.text = data["mobile"]

                self.status.text = f"✅ OCR সম্পন্ন! ({len(text)} অক্ষর)"
            except Exception as e:
                self.status.text = f"❌ OCR Error: {str(e)[:40]}"
            finally:
                Clock.schedule_once(lambda dt: setattr(self.status, 'text', "প্রস্তুত | Ready"), 4)

        Clock.schedule_once(do_ocr, 0.5)

    def save_excel(self, instance):
        if not self.name.text.strip():
            self.status.text = "❌ নাম দিন!"
            return
        if not self.voucher.text.strip():
            self.status.text = "❌ ভাউচার নম্বর দিন!"
            return
        if not self.amount.text.strip():
            self.status.text = "❌ টাকার পরিমাণ দিন!"
            return

        now = datetime.now()
        self.excel.save_data(
            self.name.text.strip(),
            self.voucher.text.strip(),
            self.amount.text.strip(),
            self.mobile.text.strip(),
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        )
        self.status.text = "✅ Excel-এ সেভ হয়েছে!"
        self.update_entry_count()
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "প্রস্তুত | Ready"), 3)

    def clear_fields(self, instance):
        self.name.text = ""
        self.voucher.text = ""
        self.amount.text = ""
        self.mobile.text = ""
        self.status.text = "ফিল্ড খালি করা হয়েছে"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "প্রস্তুত | Ready"), 2)

    def update_entry_count(self):
        count = self.excel.total_rows()
        self.entries_label.text = f"সাম্প্রতিক এন্ট্রি: {count}টি"


class VoucherApp(App):
    def build(self):
        return VoucherScanner()


if __name__ == "__main__":
    VoucherApp().run()
