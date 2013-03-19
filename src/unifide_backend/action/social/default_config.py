#default config (do not edit these)
import os

here = os.path.realpath(__file__)

#always try to use base config if they exist
try:
    from unifide_backend.local_config import *
except ImportError:
    pass