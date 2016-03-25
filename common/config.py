"""Config File Handler"""
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# pylint: disable=invalid-name
_config = configparser.SafeConfigParser()
_config.read([
    'config/py4finopt.cfg',
    os.path.join(os.path.expanduser('~'), '.py4finopt.cfg')])

# funcs not consts
get = _config.get
getint = _config.getint
getfloat = _config.getfloat
getboolean = _config.getboolean


def getlist(x, y):
    return get(x, y).split(',')


class Section(object):

    """Section within a config file"""

    def __init__(self, name):
        self.name = name

    def get(self, option):
        """Get a value in the section as a string"""
        return get(self.name, option)

    def getint(self, option):
        """Get a value in the section as an int"""
        return getint(self.name, option)

    def getfloat(self, option):
        """Get a value in the section as a float"""
        return getfloat(self.name, option)

    def getboolean(self, option):
        """Get a value in the section as a boolean"""
        return getboolean(self.name, option)

    def getlist(self, option):
        """Get a value in the section as a list (comma separated)"""
        return getlist(self.name, option)
