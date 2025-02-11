import sys
from .version import __version__
from .inspection.inspection import wat

__all__ = [
    'wat',
    '__version__'
]

sys.modules[__name__] = wat
wat.__version__ = __version__