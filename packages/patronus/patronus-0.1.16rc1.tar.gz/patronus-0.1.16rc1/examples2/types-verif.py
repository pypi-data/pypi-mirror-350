import collections

import functools

import inspect


def arg_logger(fn):
    sig = inspect.signature(fn)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"AM I Method? {inspect.ismethodwrapper(fn)}")
        print(sig.parameters)
        b_args = sig.bind(*args, **kwargs)
        print(isinstance(b_args.arguments, collections.OrderedDict))
        print(b_args.arguments)
        b_args.arguments.popitem()
        print(b_args.arguments)

    return wrapper


class Bar:
    @arg_logger
    def foo(self, x, y, *, foo=None, bar=None): ...


Bar().foo(1, 2, foo="foo", bar="bar")
