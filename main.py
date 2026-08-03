from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.camera import Camera

from datetime import datetime
import os
import csv
import random


class VoucherScanner(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=8, **kwargs)
        Window.softinput_mode = "below_target"

        self.csv_file = "vouchers.csv"
        self._ensure_csv()

        self.add_widget(Label(
            text="[b]VOUCHER SCANNER[/b]",
            markup=True,
            size_hint=(1, 0.06),
            color=(0.2, 0.6, 1, 1),
            font_size="20sp"
        ))

        self.camera = Camera(play=False, resolution=(640, 480))
        self.camera.size_hint = (1, 0.26)
        self.add_widget(self.camera)

        self.status = Label(
            text="Tap 'Start Camera'",
            size_hint=(1, 0.05),
            color=(0.3, 0.7, 0.3, 1),
            bold=True,
            font_size="14sp"
        )
        self.add_widget(self.status)

        self.name = TextInput(hint_text="Child Name", multiline=False, size_hint=(1, 0.07), font_size="15sp")
        self.add_widget(self.name)

        self.voucher = TextInput(hint_text="Voucher Number", multiline=False, size_hint=(1, 0.07), font_size="15sp")
        self.add_widget(self.voucher)

        self.amount = TextInput(hint_text="Amount (Tk)", multiline=False, input_filter="float", size_hint=(1, 0.07), font_size="15sp")
        self.add_widget(self.amount)

        self.mobile = TextInput(hint_text="Mobile Number", multiline=False, size_hint=(1, 0.07), font_size="15sp")
        self.add_widget(self.mobile)

        btn_grid = GridLayout(cols=2, size_hint=(1, 0.24), spacing=8)

        btn_start = Button(text="[b]Start Cam[/b]", markup=True, background_color=(0.2, 0.5, 0.9, 1), color=(1,1,1,1), font_size="14sp")
        btn_start.bind(on_press=self.start_cam)
        btn_grid.add_widget(btn_start)

        btn_scan = Button(text="[b]Capture & Scan[/b]", markup=True, background_color=(0.9, 0.5, 0.2, 1), color=(1,1,1,1), font_size="14sp")
        btn_scan.bind(on_press=self.capture_and_scan)
        btn_grid.add_widget(btn_scan)

        btn_save = Button(text="[b]SAVE[/b]", markup=True, background_color=(0.2, 0.7, 0.3, 1), color=(1,1,1,1), font_size="14sp")
        btn_save.bind(on_press=self.save)
        btn_grid.add_widget(btn_save)

        btn_fill = Button(text="[b]Demo Fill[/b]", markup=True, background_color=(0.5, 0.3, 0.7, 1), color=(1,1,1,1), font_size="14sp")
        btn_fill.bind(on_press=self.demo_fill)
        btn_grid.add_widget(btn_fill)

        btn_view = Button(text="[b]View All[/b]", markup=True, background_color=(0.2, 0.5, 0.9, 1), color=(1,1,1,1), font_size="14sp")
        btn_view.bind(on_press=self.view_all)
        btn_grid.add_widget(btn_view)

        btn_clear = Button(text="[b]Clear[/b]", markup=True, background_color=(0.7, 0.2, 0.2, 1), color=(1,1,1,1), font_size="14sp")
        btn_clear.bind(on_press=self.clear)
        btn_grid.add_widget(btn_clear)

        self.add_widget(btn_grid)

        self.entries_label = Label(text="Total Entries: 0", size_hint=(1, 0.05), color=(0.5, 0.5, 0.5, 1), font_size="13sp")
        self.add_widget(self.entries_label)
        self.update_count()

        self.data_label = Label(
            text="", size_hint=(1, None), height=120,
            color=(0.8, 0.8, 0.8, 1), font_size="12sp",
            markup=True, halign="left", valign="top"
        )
        self.data_label.bind(width=lambda *x: self.data_label.setter('text_size')(self.data_label, (self.data_label.width, None)))
        scroll = ScrollView(size_hint=(1, 0.14))
        scroll.add_widget(self.data_label)
        self.add_widget(scroll)

    def _ensure_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Voucher", "Amount", "Mobile", "Date", "Time"])

    def start_cam(self, instance):
        try:
            self.camera.play = True
            self.status.text = "Camera ON"
        except Exception as e:
            self.status.text = "Camera failed"

    def capture_and_scan(self, instance):
        try:
            os.makedirs("captures", exist_ok=True)
            fname = datetime.now().strftime("%Y%m%d_%H%M%S.png")
            fpath = os.path.join("captures", fname)
            self.camera.export_to_png(fpath)
            self.camera.play = False
            self.status.text = "Scanning..."
            Clock.schedule_once(lambda dt: self._run_ocr_demo(), 0.5)
        except Exception as e:
            self.status.text = "Capture failed"
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 3)

    def _run_ocr_demo(self):
        vouchers = ["V-10258", "V-20491", "V-31572", "V-44830", "V-56129"]
        names = ["Rahim Uddin", "Karim Ali", "Salma Begum", "Jamal Hossain", "Fatima Khatun"]
        amounts = ["1500", "2200", "850", "3000", "1750"]
        mobiles = ["01712345678", "01898765432", "01611223344", "01955667788", "01599887766"]
        idx = random.randint(0, 4)
        self.name.text = names[idx]
        self.voucher.text = vouchers[idx]
        self.amount.text = amounts[idx]
        self.mobile.text = mobiles[idx]
        self.status.text = "Scanned! Edit & Save"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 4)

    def demo_fill(self, instance):
        self.name.text = "Rahim Uddin"
        self.voucher.text = "V-10258"
        self.amount.text = "1500"
        self.mobile.text = "01712345678"
        self.status.text = "Demo filled!"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 2)

    def save(self, instance):
        if not self.name.text.strip() or not self.voucher.text.strip() or not self.amount.text.strip():
            self.status.text = "Fill required!"
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
            self.clear(None)
            self.update_count()
        except Exception as e:
            self.status.text = "Save error"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 3)

    def clear(self, instance):
        self.name.text = ""
        self.voucher.text = ""
        self.amount.text = ""
        self.mobile.text = ""
        self.data_label.text = ""
        if instance:
            self.status.text = "Cleared"
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 2)

    def view_all(self, instance):
        try:
            rows = []
            with open(self.csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for i, row in enumerate(reader, 1):
                    if row:
                        rows.append(f"{i}. {row[0]} | {row[1]} | Tk{row[2]}")
            if rows:
                self.data_label.text = "\n".join(rows[-8:])
                self.status.text = f"Total: {len(rows)}"
            else:
                self.data_label.text = "No records"
                self.status.text = "No data"
        except:
            self.data_label.text = "Error"
            self.status.text = "Error"
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "Ready"), 3)

    def update_count(self):
        try:
            count = 0
            with open(self.csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for _ in reader:
                    count += 1
            self.entries_label.text = f"Total Entries: {count}"
        except:
            self.entries_label.text = "Total Entries: 0"


class VoucherApp(App):
    def build(self):
        return VoucherScanner()


if __name__ == "__main__":
    VoucherApp().run()
