from functools import wraps

class CacheMiss(Exception):
    pass

class Cache(object):
    def __init__(self, func):
        self.func = func
        self.use_cache = True

    def __call__(self, *args):
        res = None
        # If we want to use the cache, do it
        if self.use_cache:
            try:
                res = self.__check_cache(args)
                print("Found in Cache!!", res)
            except CacheMiss, e:
                # Cache miss, so we need to fetch
                res = self.func(args)
            finally:
                # Want to update the cache
                self.__write_cache(res, args)
        else:
            # Caching turned off, ignore current cache state
            # and don't write back
            res = self.__fetch_result(args)
        return res

    def __check_cache(self, *args):
        raise CacheMiss()
        #raise NotImplementedError()

    def __write_cache(self, res, args):
        #raise NotImplementedError()
        pass

class CacheWrapperTest(CacheWrapper):
    def __init__(self, func):
        super(CacheWrapperTest, self).__init__(func)
        self.cache = {}

    def __check_cache(self, *args):
        try:
            print "Here"
            return self.cache[args]
        except KeyError, e:
            raise CacheMiss()
    
    def __write_cache(self, res, args):
        self.cache[args] = res

@CacheWrapperTest
def test_case_simple(a):
    return 2*a

@CacheWrapperTest
def test_case_args(*args):
    return sum(args)

@CacheWrapperTest
def test_case_fac(f):
    if f == 0:
        return 1
    elif f > 0:
        return f*test_case_fac(f-1)
    else:
        raise ValueError()

if __name__ == '__main__':
    tc = CacheWrapperTest(test_case_simple)

    for i in range(100):
        for _ in range(2):
            assert 2*i == tc.__call__(i)
    print test_case_args(1, 2, 3)
    print test_case_args(1, 2, 3)
    print test_case_fac(1000)
    print test_case_fac(10000)
    print test_case_fac(10001)



