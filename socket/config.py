import os
_basedir = os.path.abspath(os.path.dirname(__file__))

try:
    from local_config import *
except ImportError:
    pass
