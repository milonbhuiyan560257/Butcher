from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.textinput import TextInput

from excel import ExcelManager

from datetime import datetime
import os


class VoucherScanner(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.excel = ExcelManager()

        # Camera
        self.camera = Camera(
            play=True,
            resolution=(1280, 720)
        )
        self.add_widget(self.camera)

        # Status
        self.status = Label(
            text="Ready",
            size_hint=(1, 0.08)
        )
        self.add_widget(self.status)

        # Name
        self.name = TextInput(
            hint_text="Child Name",
            multiline=False,
            size_hint=(1, 0.08)
        )
        self.add_widget(self.name)

        # Voucher
        self.voucher = TextInput(
            hint_text="Voucher Number",
            multiline=False,
            size_hint=(1, 0.08)
        )
        self.add_widget(self.voucher)

        # Amount
        self.amount = TextInput(
            hint_text="Amount",
            multiline=False,
            size_hint=(1, 0.08)
        )
        self.add_widget(self.amount)

        # Capture Button
        btn_capture = Button(
            text="Capture Image",
            size_hint=(1, 0.09)
        )
        btn_capture.bind(on_press=self.capture)
        self.add_widget(btn_capture)

        # Save Button
        btn_save = Button(
            text="Save Excel",
            size_hint=(1, 0.09)
        )
        btn_save.bind(on_press=self.save_excel)
        self.add_widget(btn_save)

        # OCR Button
        btn_ocr = Button(
            text="Start OCR",
            size_hint=(1, 0.09)
        )
        btn_ocr.bind(on_press=self.start_ocr)
        self.add_widget(btn_ocr)

    def capture(self, instance):

        os.makedirs("captures", exist_ok=True)

        filename = "captures/voucher.png"

        self.camera.export_to_png(filename)

        self.status.text = "Image Saved"

    def save_excel(self, instance):

        now = datetime.now()

        self.excel.save_data(
            self.name.text,
            self.voucher.text,
            self.amount.text,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        )

        self.status.text = "Saved To Excel"

    def start_ocr(self, instance):

        self.status.text = "OCR Module Coming Soon"


class VoucherApp(App):

    def build(self):
        return VoucherScanner()


if __name__ == "__main__":
    VoucherApp().run()
