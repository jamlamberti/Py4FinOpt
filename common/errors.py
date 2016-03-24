"""Custom errors that can be thrown"""


class InvalidCacheOption(Exception):

    """
    Used for when we can't support the
    cache option specified in the config file
    """
    pass


class CacheMiss(Exception):

    """Throw whenever there is a cache miss"""
    pass
