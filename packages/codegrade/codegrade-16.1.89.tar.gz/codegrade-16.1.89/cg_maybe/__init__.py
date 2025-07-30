"""This module implements the ``Maybe`` monad.
"""
from . import utils
from ._just import Just
from .utils import of, from_nullable
from ._maybe import Maybe
from ._nothing import Nothing, _Nothing
