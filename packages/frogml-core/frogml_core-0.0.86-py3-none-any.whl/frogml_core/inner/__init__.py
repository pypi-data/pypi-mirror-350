"""Top-level package for frogml-proto."""

# fmt: off
__author__ = '''Frogml'''
__email__ = 'info@frogml.com'
__version__ = '0.0.315.dev0'
# fmt: on

from .di_configuration import wire_dependencies

_container = wire_dependencies()
