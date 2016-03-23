"""Memoize Implementation"""

from common.errors import CacheMiss

class MemoizedDict(object):
    """Memoize implementation using decorators and a dictionary"""
    # pylint: disable=too-few-public-methods
    def __init__(self, func, use_cache=True):
        self.func = func
        self.use_cache = use_cache
        self.cache = {}

    def __call__(self, *args):
        """call wrapper for func to memoize"""
        res = None
        if self.use_cache:
            try:
                res = self.__check_cache(args)
                print("Found in cache!!!", res)
            except CacheMiss:
                res = self.func(*args)
                self.__write_cache(res, args)
        else:
            res = self.func(*args)
        return res

    def __check_cache(self, args):
        """check for cache hit, throw cache miss on miss"""
        try:
            return self.cache[args]
        except KeyError:
            raise CacheMiss()

    def __write_cache(self, res, args):
        """write result to dict"""
        self.cache[args] = res

@MemoizedDict
def simple_test(arg):
    """Smoke test of memoized dict"""
    return 2*arg

if __name__ == '__main__':
    for i in range(10):
        for _ in range(2):
            assert 2*i == simple_test(i)
