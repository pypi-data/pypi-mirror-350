import threading


def singleton(cls, *args, **kw):
    instances = {}
    lock = threading.Lock()

    def _singleton(*args, **kw):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton
