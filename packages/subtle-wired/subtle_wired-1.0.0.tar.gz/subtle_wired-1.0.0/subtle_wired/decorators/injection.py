__author__ = 'Willian Antonio'

from subtle_wired.core.injector import InjectedItem, Injector


def inject(func):
    if func.__name__ == '__init__':
        return InjectedItem.get_init_wrapper(func, Injector())
    else:
        return InjectedItem.get_method_wrapper(func, Injector())


class inject_property(property):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return InjectedItem.get_method_wrapper(self.func, Injector())(instance)

    def __set__(self, instance, value):
        raise AttributeError(
            f"Cannot set attribute '{self.func.__name__}' on '{instance.__class__.__name__}'. "
            'This property is read-only (populated by the container)!'
        )
