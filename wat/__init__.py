import sys

from .inspection.inspection import wat

from .version import __version__

sys.modules[__name__] = wat
wat.__version__ = __version__

# Adding __all__ declaration to define the public interface
__all__ = ['wat']