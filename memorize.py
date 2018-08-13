#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import functools
import datetime
from random import randint
from time import sleep


def memorize(ttl):
    '''
    memorize decorator with TTL to temporarily cache results
    '''
    def memorize_decorator(func):
        cached = dict()

        @functools.wraps(func)
        def memorize_func(*args, **kwargs):
            now = datetime.datetime.now()
            key = str(args) + str(kwargs)
            res = cached.get(key)
            if res:
                until, res = res
                if until >= now:
                    return res
            # result not found or timed out
            until = now + datetime.timedelta(seconds=ttl)
            res = func(*args, **kwargs)
            cached[key] = until, res
            return res
        return memorize_func
    return memorize_decorator


@memorize(10)
def weakrandom(vmin, vmax):
    return randint(vmin, vmax)


if __name__ == "__main__":
    try:
        while True:
            print(weakrandom(1, 100))
            sleep(1)
    except KeyboardInterrupt:
        pass
