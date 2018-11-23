# -*- coding: utf-8 -*-
from src.Config.manager import Manager
from imutils.video import VideoStream


class FrameSource:
    def __init__(self, config=Manager()):
        self.config = config
        if not self.config.isLoaded():
            self.config.load()
        src = int(self.config.get("CAMERA:device"))
        picam = self.config.getBool("CAMERA:picam")
        res = self.decodeResolution(self.config.get("CAMERA:resolution"))
        fps = int(self.config.get("CAMERA:framerate"))
        self.stream = VideoStream(src=src, usePiCamera=picam, resolution=res, framerate=fps)

    def decodeResolution(self, resolution=""):
        if "p" == resolution[-1].lower():
            resolutions = {"120": (160, 120),
                           "160": (240, 160),
                           "200": (320, 200),
                           "240": (320, 240),
                           "300": (400, 300),
                           "320": (480, 320),
                           "350": (640, 350),
                           "480": (640, 480),
                           "600": (800, 600)}
            return resolutions[resolution[:-1]]
        elif "x" in resolution.lower():
            return resolution.split("x")

# TODO: code the rest of the functions needed