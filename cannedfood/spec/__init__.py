
__all__ = [ "config", "messages", "nodes", "util" ]

from config import CanSpecConfig

def load_config(fn):
    return CanSpecConfig(fn)
