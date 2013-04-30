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

Document attributes and data
----------------------------
As you know a :py:class:`~djamo.document.Document` is a subclass of Python dictionary. You can access to your document data (dictionary data) like a normal Python dictionary,
also **Djamo** provides another way to make development easier. You can use instance attributes to reference your corresponding key in your document dictionary just like::

    class Strudent(Document):
        pass

    new_student = Student()

    # Set a name to new_student using dictionary approach
    new_student['name'] = "Asuma"

    # Set Asuma's age using instance attributes approach
    new_student.age = 22

As you can see **Djamo** made it easy to use documents. But there is a limitation about using instance attributes approach. If you have a class or instance variable in your
instance before with the same name of your new key, **Djamo** will assign the value to class or instance variable of your document instead of the key. let see an example::

    class Student(Document):
        # A class variable to use in internal Student document internals
	log_msg = ""

    student = Student()

    # Set the new key / value to document using instance attribute approach
    student.log_msg = "Some value for dictionary DATA"

    student.keus()  # result ->  []

In the above example you can see that using instance attribute to set a new key "log_msg" with value of "Some value for dictionary DATA" into ``student`` document, but why ``student.keys()``
return an empty list? The answer is simple, because there is a property in **Student** class with the name of "log_msg" and using instance attribute to set a value cause setting value to
``log_msg`` attribute instead of creating new key to dictionary.
