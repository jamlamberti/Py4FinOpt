import functools
from common import config
class CacheMiss(Exception):
    pass

class MemoizedDict(object):
    def __init__(self, func, use_cache=True):
        self.func = func
        self.use_cache = use_cache
        self.cache = {}

    def __call__(self, *args):
        res = None
        if self.use_cache:
            try:
                res = self.__check_cache(args)
                print("Found in cache!!!", res)
            except CacheMiss, e:
                res = self.func(*args)
                self.__write_cache(res, args)
        else:
            res = self.func(*args)
        return res

    def __check_cache(self, args):
        try:
            return self.cache[args]
        except KeyError, e:
            raise CacheMiss()

    def __write_cache(self, res, args):
        self.cache[args] = res

@MemoizedDict
def simple_test(a):
    return 2*a

if __name__ == '__main__':
    for i in range(10):
        for _ in range(2):
            assert 2*i == simple_test(i)
