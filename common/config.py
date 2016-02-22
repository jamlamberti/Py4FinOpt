import os
import ConfigParser

_config = ConfigParser.SafeConfigParser()
_config.read(['config/py4finopt.cfg', os.path.join(os.path.expanduser('~'), '.py4finopt.cfg')])

get = _config.get
getint = _config.getint
getfloat = _config.getfloat
getboolean = _config.getboolean
getlist = lambda x,y: get(x, y).split(',')

class Section(object):
    def __init__(self, name):
        self.name = name

    def get(self, option):
        return get(self.name, option)

    def getint(self, option):
        return getint(self.name, option)

    def getfloat(self, option):
        return getfloat(self.name, option)

    def getboolean(self, option):
        return getboolean(self.name, option)

    def getlist(self, option):
        return getlist(self.name, option)

