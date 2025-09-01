from importlib import import_module
import sys

module = import_module("app")
sys.modules[__name__] = module
