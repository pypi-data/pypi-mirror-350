#
#
from pybasics.logs import info, warn, ok

def method_log(func):
    def func_wrapper(*args,**kwargs):
        warn('Start: %s' % func.__qualname__)
        result = func(*args,**kwargs)
        ok('End: %s' % func.__qualname__)
        return result
    return func_wrapper
