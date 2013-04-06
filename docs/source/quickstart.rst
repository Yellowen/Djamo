Djamo Quick Start Guide
=======================
**Djamo** API is very similar to `PyMmongo <http://api.mongodb.org/python/current/>`_, But **Djamo** provides an OOP way to use PyMongo.


Let's begin
-----------
**Djamo** tries to stay as simple as possible, so it's very easy to use it. Djamo provides two main class to represent your data model. :py:class:`~djamo.document.Document` is the base class for representing a MongoDB document. :py:class:`~djamo.document.Document` is a **dict**
subclass and it's optional to use it, You can simply use a dictionary just like the way PyMongo do, But using :py:class:`~djamo.document.Document` brings you some useful advantages. For example you can
 specify a ``fileds`` property for your :py:class:`~djamo.document.Document`, **Djamo** will use it for validate and serialize your data (Don't worry you will learn it soon).

Other useful class is :py:class:`~djamo.collection.Collection` which represent a MongoDB collection. As i told earlier in this document **Djamo** has a API very similar to  **PyMongo**'s. So :py:class:`~djamo.collection.Collection` is a subclass of PyMongo Collection and share the same methods as PyMongo.

Let's see some examples, Here is a simple Document/Collection to represent a Student data::

    From djamo import Collection, Document


    Class Student (Document):
        pass


    Class Students (Collection):
       document = Student

It's easy, isn't it? The `Student` class is document with no specific property and `Students` class is a collection that use `Student` document as its default document. Each collection should define a ``document`` attribute which used for serializing and de-serializing collection data, if no document specified **Djamo** will use normal python dictionary to work with collections data. Now its time to use above
code and insert data into database.
