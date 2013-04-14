Djamo Collection Implementation
===============================

.. automodule:: djamo.collections
   :members:

.. seealso:: Since :py:class: `~djamo.collections.BaseCollection` is a subclass of PyMongos Collection class, and we don't document the methods that does not overridden, it will be heplful
             for you to take a look at `PyMongo Collection <http://api.mongodb.org/python/current/api/pymongo/collection.html>`_ document too.

BaseCollection class
--------------------
This collection class is the base of other **Djamo** collections and contains the same interface as **PyMongo**.

.. autoclass:: djamo.collections.BaseCollection
   :members:
   :private-members:


Collection class
----------------
This class is contains all the methods that are wrappers to  **PyMongo** interface or PyMongo did not provided.

.. autoclass:: djamo.collections.Collection
   :members:
   :private-members:
