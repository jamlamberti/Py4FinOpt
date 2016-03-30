"""Memoize Implementation"""

from common.errors import CacheMiss


class MemoizedDict(object):

    """Memoize implementation using decorators and a dictionary"""
    # pylint: disable=too-few-public-methods

    def __init__(self, use_cache=True):
        self.use_cache = use_cache
        self.cache = {}

    def __call__(self, func, *args):
        def new_func(*args):
            """call wrapper for func to memoize"""
            res = None
            if self.use_cache:
                try:
                    res = self.__check_cache(args)
                    print("Found in cache!!!", res)
                except CacheMiss:
                    res = func(*args)
                    self.__write_cache(res, args)
            else:
                res = func(*args)
            return res
        return new_func

    def __check_cache(self, args):
        """check for cache hit, throw cache miss on miss"""
        try:
            return self.cache[args]
        except KeyError:
            raise CacheMiss()

    def __write_cache(self, res, args):
        """write result to dict"""
        self.cache[args] = res
