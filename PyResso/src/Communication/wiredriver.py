from serial import *
from src.Config.manager import Manager


class WireDriver:
    def __init__(self, conf=Manager()):
        self.conf = conf
        if not self.conf.isLoaded():
            self.conf.load()
        self.ser = Serial()
        self.ser.baudrate = conf.get("SERIAL:baud")
        self.ser.port = conf.get("SERIAL:port")
        try:
            self.ser.open()
            self.open = True
        except SerialException:
            self.open = False
            print("unable to open device!")

    def send(self, text=""):
        if text[-1] != "\n":
            text += "\n"
        # print(text)
        if self.open:
            self.ser.write(bytes(text.encode()))
            string = self.ser.readline()
            print(string)
        else:
            print("Could not send command, because the port is not open!")

    def __del__(self):
        if self.open:
            self.ser.close()
