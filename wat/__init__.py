from .version import __version__
from .inspection.inspection import wat

__all__ = ['wat', '__version__']

import sys
sys.modules[__name__] = wat