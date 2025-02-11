__version__ = "0.1.2"  # should be in sync with pyproject.toml

def __getattr__(name):
    if name == 'wat':
        return self
    raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")