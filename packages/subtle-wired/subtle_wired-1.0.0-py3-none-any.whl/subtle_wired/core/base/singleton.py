__author__ = 'Willian Antônio'

from threading import Lock


class SingletonMeta(type):
    """Class to implement singleton type."""

    def __init__(cls, name, bases, dct):
        super(SingletonMeta, cls).__init__(name, bases, dct)
        cls._instance = None
        cls._lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SingletonMeta, cls).__call__(
                    *args, **kwargs
                )
        return cls._instance


class Singleton(object, metaclass=SingletonMeta):
    """Class to implement singleton."""

    def __init__(self):
        super(Singleton, self).__init__()
