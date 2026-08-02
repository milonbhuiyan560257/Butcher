from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

from datetime import datetime
import os
import csv


class VoucherScanner(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=10, **kwargs)
        Window.softinput_mode = "below_target"

        self.csv_file = "vouchers.csv"
        self._ensure_csv()

        self.add_widget(Label(
            text="[b]VOUCHER SCANNER[/b]",
            markup=True,
            size_hint=(1, 0.08),
            color=(0.2, 0.6, 1, 1),
            font_size="22sp"
        ))

        self.status = Label(
            text="Ready",
            size_hint=(1, 0.06),
            color=(0.3, 0.7, 0.3, 1),
            bold=True
        )
        self.add_widget(self.status)

        self.name = TextInput(hint_text="Child Name", multiline=False, size_hint=(1, 0.08), font_size="16sp")
        self.add_widget(self.name)

        self.voucher = TextInput(hint_text="Voucher Number", multiline=False, size_hint=(1, 0.08), font_size="16sp")
        self.add_widget(self.voucher)

        self.amount = TextInput(hint_text="Amount (Tk)", multiline=False, input_filter="float", size_hint=(1, 0.08), font_size="16sp")
        self.add_widget(self.amount)

        self.mobile = TextInput(hint_text="Mobile Number", multiline=False, size_hint=(1, 0.08), font_size="16sp")
        self.add_widget(self.mobile)

        btn_grid = GridLayout(cols=2, size_hint=(1, 0.18), spacing=10)

        btn_save = Button(text="[b]SAVE[/b]", markup=True, background_color=(0.2, 0.7, 0.3, 1), color=(1,1,1,1), font_size="16sp")
        btn_save.bind(on_press=self.save)
        btn_grid.add_widget(btn_save)

        btn_fill = Button(text="[b]DEMO FILL[/b]", markup=True, background_color=(0.9, 0.5, 0.2, 1), color=(1,1,1,1), font_size="16sp")
        btn_fill.bind(on_press=self.demo_fill)
        btn_grid.add_widget(btn_fill)

        btn_view = Button(text="[b]VIEW ALL[/b]", markup=True, background_color=(0.2, 0.5, 0.9, 1), color=(1,1,1,1), font_size="16sp")
        btn_view.bind(on_press=self.view_all)
        btn_grid.add_widget(btn_view)

        btn_clear = Button(text="[b]CLEAR[/b]", markup=True, background_color=(0.7, 0.2, 0.2, 1), color=(1,1,1,1), font_size="16sp")
        btn_clear.bind(on_press=self.clear)
        btn_grid.add_widget(btn_clear)

        self.add_widget(btn_grid)

        self.entries_label = Label(text="Total Entries: 0", size_hint=(1, 0.06), color=(0.4, 0.4, 0.4, 1), font_size="14sp")
        self.add_widget(self.entries_label)
        self.update_count()

        self.data_label = Label(text="", size_hint=(1, None), height=200, color=(0.2, 0.2, 0.2, 1), font_size="12sp", markup=True, halign="left", valign="top")
        self.data_label.bind(width=lambda *x: self.data_label.setter('text_size')(self.data_label, (self.data_label.width, None)))
        
        scroll = ScrollView(size_hint=(1, 0.25))
        scroll.add_widget(self.data_label)
        self.add_widget(scroll)

    def _ensure_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Voucher", "Amount", "Mobile", "Date", "Time"])

    def demo_fill(self, instance):
        self.name.text = "Rahim Uddin"
        self.voucher.text = "V-10258"
        self.amount.text = "1500"
        self.mobile.text = "01712345678"
        self.status.text = "Demo data filled!"
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
            self.status.text = "Saved successfully!"
            self.clear(None)
            self.update_count()
        except Exception as e:
            self.status.text = f"Error: {str(e)[:30]}"
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
                self.data_label.text = "\n".join(rows[-10:])
                self.status.text = f"Showing {len(rows)} records"
            else:
                self.data_label.text = "No records yet"
                self.status.text = "No data"
        except Exception as e:
            self.data_label.text = f"Error: {str(e)[:50]}"
            self.status.text = "Error loading data"
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
