from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.camera import Camera

from datetime import datetime
import os
import csv


class VoucherScanner(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=5, **kwargs)
        Window.softinput_mode = "below_target"

        self.csv_file = "vouchers.csv"
        self._ensure_csv()

        # Camera (stopped initially)
        self.camera = Camera(play=False, resolution=(640, 480))
        self.camera.size_hint = (1, 0.35)
        self.add_widget(self.camera)

        # Status
        self.status = Label(
            text="Tap 'Start Camera'",
            size_hint=(1, 0.06),
            color=(0.2, 0.6, 1, 1),
            bold=True
        )
        self.add_widget(self.status)

        # Inputs
        self.name = TextInput(hint_text="Name", multiline=False, size_hint=(1, 0.07))
        self.add_widget(self.name)

        self.voucher = TextInput(hint_text="Voucher No", multiline=False, size_hint=(1, 0.07))
        self.add_widget(self.voucher)

        self.amount = TextInput(hint_text="Amount", multiline=False, input_filter="float", size_hint=(1, 0.07))
        self.add_widget(self.amount)

        self.mobile = TextInput(hint_text="Mobile", multiline=False, size_hint=(1, 0.07))
        self.add_widget(self.mobile)

        # Buttons
        btn_grid = GridLayout(cols=2, size_hint=(1, 0.20), spacing=5)

        btn_start = Button(text="Start Cam", background_color=(0.2, 0.5, 0.9, 1), color=(1,1,1,1))
        btn_start.bind(on_press=self.start_cam)
        btn_grid.add_widget(btn_start)

        btn_cap = Button(text="Capture", background_color=(0.1, 0.4, 0.8, 1), color=(1,1,1,1))
        btn_cap.bind(on_press=self.capture)
        btn_grid.add_widget(btn_cap)

        btn_ocr = Button(text="Auto Fill", background_color=(0.9, 0.5, 0.2, 1), color=(1,1,1,1))
        btn_ocr.bind(on_press=self.auto_fill)
        btn_grid.add_widget(btn_ocr)

        btn_save = Button(text="Save", background_color=(0.2, 0.7, 0.3, 1), color=(1,1,1,1))
        btn_save.bind(on_press=self.save)
        btn_grid.add_widget(btn_save)

        btn_clear = Button(text="Clear", background_color=(0.7, 0.2, 0.2, 1), color=(1,1,1,1))
        btn_clear.bind(on_press=self.clear)
        btn_grid.add_widget(btn_clear)

        btn_view = Button(text="View Data", background_color=(0.5, 0.2, 0.7, 1), color=(1,1,1,1))
        btn_view.bind(on_press=self.view_data)
        btn_grid.add_widget(btn_view)

        self.add_widget(btn_grid)

        self.entries_label = Label(text="Entries: 0", size_hint=(1, 0.05))
        self.add_widget(self.entries_label)
        self.update_count()

    def _ensure_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Voucher", "Amount", "Mobile", "Date", "Time"])

    def start_cam(self, instance):
        try:
            self.camera.play = True
            self.status.text = "Camera ON"
        except:
            self.status.text = "Camera failed"

    def capture(self, instance):
        try:
            os.makedirs("captures", exist_ok=True)
            fname = datetime.now().strftime("%Y%m%d_%H%M%S.png")
            fpath = os.path.join("captures", fname)
            self.camera.export_to_png(fpath)
            self.camera.play = False
            self.status.text = "Photo saved!"
            self._last_photo = fpath
        except Exception as e:
            self.status.text = "Capture failed"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 2)

    def auto_fill(self, instance):
        self.name.text = "Rahim Uddin"
        self.voucher.text = "V-10258"
        self.amount.text = "1500"
        self.mobile.text = "01712345678"
        self.status.text = "Auto-filled!"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 2)

    def save(self, instance):
        if not self.name.text.strip() or not self.voucher.text.strip() or not self.amount.text.strip():
            self.status.text = "Fill required fields!"
            return
        try:
            now = datetime.now()
            with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    self.name.text.strip(),
                    self.voucher.text.strip(),
                    self.amount.text.strip(),
                    self.mobile.text.strip(),
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S")
                ])
            self.status.text = "Saved!"
            self.update_count()
        except Exception as e:
            self.status.text = "Save error"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 2)

    def clear(self, instance):
        self.name.text = ""
        self.voucher.text = ""
        self.amount.text = ""
        self.mobile.text = ""
        self.status.text = "Cleared"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 2)

    def view_data(self, instance):
        try:
            count = 0
            with open(self.csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    count += 1
            self.status.text = f"Total records: {count}"
        except:
            self.status.text = "No data"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 3)

    def update_count(self):
        try:
            count = 0
            with open(self.csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for _ in reader:
                    count += 1
            self.entries_label.text = f"Entries: {count}"
        except:
            self.entries_label.text = "Entries: 0"


class VoucherApp(App):
    def build(self):
        return VoucherScanner()


if __name__ == "__main__":
    VoucherApp().run()
