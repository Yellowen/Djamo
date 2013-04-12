"""
**Documents** by themselves does not have ability to save to database. To do
that you should use a ``collection`` object. Its easy to use collections
by subclassing the ``Collection`` base class.
"""

from .base import BaseCollection
from .collection import Collection
