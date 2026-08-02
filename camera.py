import os
from datetime import datetime

from kivy.uix.camera import Camera


class CameraManager:

    def __init__(self):
        self.camera = Camera(
            play=True,
            resolution=(1280, 720)
        )
        self._latest_capture = None

    def get_widget(self):
        return self.camera

    def start(self):
        self.camera.play = True

    def stop(self):
        self.camera.play = False

    def capture(self, folder="captures"):
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S.png")
        filepath = os.path.join(folder, filename)

        self.camera.export_to_png(filepath)
        self._latest_capture = filepath
        return filepath

    def get_latest_capture(self):
        if self._latest_capture and os.path.exists(self._latest_capture):
            return self._latest_capture
        # Fallback: find latest in captures folder
        folder = "captures"
        if not os.path.exists(folder):
            return None
        files = [os.path.join(folder, f) for f in os.listdir(folder)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not files:
            return None
        return max(files, key=os.path.getctime)

    def set_resolution(self, width, height):
        self.camera.resolution = (width, height)

    def is_running(self):
        return self.camera.play

    def toggle(self):
        self.camera.play = not self.camera.play

    def release(self):
        self.camera.play = False
