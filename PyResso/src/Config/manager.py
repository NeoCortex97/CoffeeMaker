from configparser import ConfigParser, ExtendedInterpolation
from shutil import copy
from util.decoding import separateBy
from os.path import expanduser


class Manager:
    def __init__(self, path="/home/stefan/CoffeMaker/PyResso/configuration/default.conf"):
        self.configpath = path
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.loaded = False

    def load(self):
        self.config.read(self.configpath)
        if len(self.config.sections()) == 0:
            print("copying default configuration . . .")
            copy("configuration/Template.conf", "configuration/default.conf")
            self.load()
        else:
            self.loaded = True
            return True

    def get(self, path=""):
        section = separateBy(path, ":")
        key = path[len(section) + 1:]
        if section not in ("PATHS", "FILES"):
            return self.config.get(section, key)
        else:
            value = self.config.get(section, key)
            if value[0] == "~":
                return expanduser("~") + value[1:]

    def getBool(self, path=""):
        section = separateBy(path, ":")
        key = path[len(section) + 1:]
        return self.config.getboolean(section, key)

    def set(self, path="", value=""):
        section = separateBy(path, ":")
        key = path[len(section) - 1:]
        self.config.set(section, key, value)

    def isLoaded(self):
        return self.loaded