class MyClass:
    __version__ = "0.2.0"

    def __getattr__(self, name):
        if name == 'wat':
            return self
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")