import sys
from .inspection.inspection import wat
from .version import __version__

__all__ = [
    'wat',
    '__version__'
]

wat.__version__ = __version__

sys.modules[__name__] = wat