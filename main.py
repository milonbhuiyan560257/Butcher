from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window

from camera import CameraManager
from data_manager import DataManager
from ocr import OCRReader
from voucher_parser import VoucherParser

from datetime import datetime
import os


class VoucherScanner(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=5, **kwargs)
        
        Window.softinput_mode = "below_target"

        self.data_mgr = DataManager()
        self.ocr = OCRReader()
        self.parser = VoucherParser()
        self.camera_mgr = CameraManager()

        self.camera = self.camera_mgr.get_widget()
        self.camera.size_hint = (1, 0.40)
        self.add_widget(self.camera)

        self.status = Label(
            text="Ready - Tap Start Camera",
            size_hint=(1, 0.06),
            color=(0.2, 0.6, 1, 1),
            bold=True
        )
        self.add_widget(self.status)

        self.name = TextInput(
            hint_text="Child Name",
            multiline=False,
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.name)

        self.voucher = TextInput(
            hint_text="Voucher Number",
            multiline=False,
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.voucher)

        self.amount = TextInput(
            hint_text="Amount",
            multiline=False,
            input_filter="float",
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.amount)

        self.mobile = TextInput(
            hint_text="Mobile",
            multiline=False,
            size_hint=(1, 0.07),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(self.mobile)

        btn_grid = GridLayout(cols=2, size_hint=(1, 0.18), spacing=5)
        
        btn_start_cam = Button(
            text="Start Camera",
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        btn_start_cam.bind(on_press=self.start_camera)
        btn_grid.add_widget(btn_start_cam)

        btn_capture = Button(
            text="Capture",
            background_color=(0.1, 0.4, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        btn_capture.bind(on_press=self.capture)
        btn_grid.add_widget(btn_capture)

        btn_ocr = Button(
            text="Run OCR",
            background_color=(0.9, 0.5, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        btn_ocr.bind(on_press=self.run_ocr)
        btn_grid.add_widget(btn_ocr)

        btn_save = Button(
            text="Save CSV",
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        btn_save.bind(on_press=self.save_data)
        btn_grid.add_widget(btn_save)

        btn_clear = Button(
            text="Clear",
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        btn_clear.bind(on_press=self.clear_fields)
        btn_grid.add_widget(btn_clear)

        self.add_widget(btn_grid)

        self.entries_label = Label(
            text="Entries: 0",
            size_hint=(1, 0.05),
            color=(0.4, 0.4, 0.4, 1)
        )
        self.add_widget(self.entries_label)
        
        self.update_entry_count()

    def start_camera(self, instance):
        try:
            self.camera_mgr.start()
            self.status.text = "Camera started"
        except Exception as e:
            self.status.text = "Camera error - use manual entry"

    def capture(self, instance):
        try:
            os.makedirs("captures", exist_ok=True)
            filename = self.camera_mgr.capture(folder="captures")
            self.camera_mgr.stop()
            self.status.text = f"Saved: {os.path.basename(filename)}"
        except Exception as e:
            self.status.text = f"Capture failed: {str(e)[:30]}"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 3)

    def run_ocr(self, instance):
        latest_img = self.camera_mgr.get_latest_capture()
        if not latest_img or not os.path.exists(latest_img):
            self.status.text = "Take photo first!"
            return

        self.status.text = "OCR running..."
        
        def do_ocr(dt):
            try:
                text = self.ocr.extract_text(latest_img)
                if not text:
                    self.status.text = "No text found"
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

                self.status.text = "OCR Done!"
            except Exception as e:
                self.status.text = f"OCR Error: {str(e)[:30]}"
            finally:
                Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 3)

        Clock.schedule_once(do_ocr, 0.5)

    def save_data(self, instance):
        if not self.name.text.strip():
            self.status.text = "Enter name!"
            return
        if not self.voucher.text.strip():
            self.status.text = "Enter voucher!"
            return
        if not self.amount.text.strip():
            self.status.text = "Enter amount!"
            return

        try:
            now = datetime.now()
            self.data_mgr.save_data(
                self.name.text.strip(),
                self.voucher.text.strip(),
                self.amount.text.strip(),
                self.mobile.text.strip(),
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S")
            )
            self.status.text = "Saved to CSV!"
            self.update_entry_count()
        except Exception as e:
            self.status.text = f"Save failed: {str(e)[:30]}"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 3)

    def clear_fields(self, instance):
        self.name.text = ""
        self.voucher.text = ""
        self.amount.text = ""
        self.mobile.text = ""
        self.status.text = "Cleared"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 2)

    def update_entry_count(self):
        try:
            count = self.data_mgr.total_rows()
            self.entries_label.text = f"Entries: {count}"
        except:
            self.entries_label.text = "Entries: ?"


class VoucherApp(App):
    def build(self):
        return VoucherScanner()


if __name__ == "__main__":
    VoucherApp().run()
