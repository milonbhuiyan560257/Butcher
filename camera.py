# camera.py

import os
from datetime import datetime

from kivy.uix.camera import Camera


class CameraManager:

    def __init__(self):

        self.camera = Camera(
            play=True,
            resolution=(1280, 720)
        )

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

        return filepath

    def set_resolution(self, width, height):

        self.camera.resolution = (width, height)

    def is_running(self):

        return self.camera.play

    def toggle(self):

        self.camera.play = not self.camera.play

    def release(self):

        self.camera.play = False
