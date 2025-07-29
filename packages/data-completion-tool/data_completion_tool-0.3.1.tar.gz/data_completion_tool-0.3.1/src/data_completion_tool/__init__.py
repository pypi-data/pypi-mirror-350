from importlib.metadata import version

from . import dct

dct.__version__ = version("data-completion-tool")  # to have the __version__ of the package
