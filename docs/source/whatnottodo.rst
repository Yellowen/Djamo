What not to do?
===============

Each software in order to achieve its goals must sacrifice something (Its the first rule of alchemy), So **Djamo** sacrifice some features to made its usage easier. Here in this document
we will focus on them.


Document class constructor arguments
------------------------------------
.. highlight:: python

As you may know the signature of a Document constructor is like::

    def __init__(self, *args, **kwargs):
        # other piece of codes
	pass

You must not define any extra argument in a :py:func:`~djamo.document.Document` constructor, Because **Djamo** itself use the constructor in other places with the exact same
signature so if you define your own arguments Djamo will malfunction. You have to keep the signature untouched. *version 2.67*

**But I need to define some arguments, What should i do then?**
It's easy. You can use `**kwargs` to store you argument and remove it from `**kwargs` after that. just like::

    class SomeDocument(Document):

        def __init__(self, *args, **kwargs):
	    self.some_property = kwargs.pop("your_argument", None)

	    Document(Document, self).__init__(*args, **kwargs)

.. note:: There more than one way but we don't bother you with the rest.
