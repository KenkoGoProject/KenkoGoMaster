import threading


class SingletonType(type):
    """单例模式"""
    _instance_lock = threading.Lock()
    _instance = None

    def __call__(cls, *args, **kwargs) -> object:
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
