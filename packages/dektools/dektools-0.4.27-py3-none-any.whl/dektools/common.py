import datetime
from .func import FuncAnyArgs


class classproperty:
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


def rect_split(total, col_max):
    for i in range(col_max):
        col = col_max - i
        rest = total % col
        if rest == 0:
            row = total // col
            return [col for _ in range(row)]
        elif rest * 2 >= col:
            row = total // col + 1
            return [col for _ in range(row - 1)] + [rest]


def find(array, func, start=None, end=None, reverse=False):
    start = 0 if start is None else max(0, start)
    end = len(array) if end is None else min(end, len(array))
    func = FuncAnyArgs(func)
    r = range(start, end)
    if reverse:
        r = reversed(r)
    for i in r:
        if func(array[i], i, array):
            return i
    return -1


def ns2datetime(t):
    return datetime.datetime.fromtimestamp(t / 1000000000)


def xvalue(x, y):
    if y is None:
        return x
    elif isinstance(y, float):
        return x.__class__(x * y)
    else:
        return y


if __name__ == '__main__':
    print(rect_split(13, 5))
    print(rect_split(11, 5))
    print(rect_split(4, 5))
