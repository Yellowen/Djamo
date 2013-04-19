Djamo Quick Start Guide
=======================
**Djamo** API is very similar to `PyMmongo <http://api.mongodb.org/python/current/>`_, But **Djamo** provides an OOP way to use PyMongo. Let's begin

Definations and inserting data
------------------------------
.. highlight:: python

After installing **Djamo** you have to add some configuration data to ``settings.py`` file of your Djanog project. Add a settings variable called ``DJAMO`` to your settings and specify MongoDB connection information in that. for example::

    DJAMO = {
        "name": "test_database",
	"host": "localhost",   # This option is optional and its default value is 'localhost'
	"port": 27017,   # This option is optional and its default value is 27017
	"max_pool_size": 10,  # This option is optional and its default value is 10
	"max_age": 1200,  # This option is optional and its default value is 400, Djamo
	                  # will keep alive the connection for max_age seconds
    }

**Djamo** tries to stay as simple as possible, so it's very easy to use it. Djamo provides two main class to represent your data model. :py:class:`~djamo.document.Document` is the base class for representing a MongoDB document. :py:class:`~djamo.document.Document` is a **dict**
subclass and it's optional to use it, You can simply use a dictionary just like the way PyMongo do, But using :py:class:`~djamo.document.Document` brings you some useful advantages. For example you can
specify a ``fileds`` property for your :py:class:`~djamo.document.Document`, **Djamo** will use it for validate and serialize your data (Don't worry you will learn it soon).

Other useful class is :py:class:`~djamo.collection.Collection` which represent a MongoDB collection. As i told earlier in this document **Djamo** has a API very similar to  **PyMongo**'s. So :py:class:`~djamo.collection.Collection` is a subclass of PyMongo Collection and share the same methods as PyMongo.

Let's see some examples, Here is a simple Document/Collection to represent a Student::

    from djamo import Collection, Document


    class Student (Document):
        pass


    class Students (Collection):
       document = Student

It's easy, isn't it? The `Student` class is document with no specific property and `Students` class is a collection that use `Student` document as its default document. Each collection should define a ``document`` attribute which used for serializing and de-serializing collection data, if no document specified **Djamo** will use normal python dictionary to work with collections data. Now its time to use above
code and do some query on database::

    student_a = Student({"name": "Uchiha Sasuke",
                         "age": 19})

    student_b = Sudent(name="Uzumaki Naruto", age=18, uid=3975611745)

    student_c = Student()
    student_c.name = "Rock Lee"
    student_c["age"] = 21

    students = Students()
    students.insert([student_a, student_b, student_c])

Here you can see that a :py:class:`~djamo.document.Document` subclass can be initialize eather by passing a dictionary or by using keyword argyments. Also you must know about how to access your document attributes, since document is a subclass of dict
class you can access to a document attributes eather using normal dictionary indexing or class attributes.

We used :py:func:`~djamo.collections.BaseCollection.insert` method of :py:class:`~djamo.collections.Collection` to put a list of students in our database. Remember documents are ``dict`` subclass and MongoDB did not force to stick with the same keys/values for your document, so your document can have any key/value pair your want. :py:func:`~djamo.collections.BaseCollection.insert` method will return a list of ``_id``s of
the inserted documents or `None` if ``manipulate`` is False.

.. note:: Returned ``_id`` value is an instance of **Object_id** class.

After inserting data it is time to update them. Assume you want to change the ``school`` key of some students with specific ``age``::

    students = Students()
    students.update_all({"age": 18}, {"$set": {"school": "school_A"}})  # update the school field of all the students with 'age' 18
    students.update({"age": 18}, {"$set": {"school": "school_A"}})  # update the school field of the first student with 'age' 18

In above example we used :py:func:`~djamo.collection.Collection.update` to change the value of ``school`` key of all the students in the ``Students`` collection who are 18 years old, to ``school_A``. If they don't have a ``school`` key it will be created.

.. note:: Remember that **update()** only updatest he first matching document **by default** if you want to update all the documents you have to set the 'multi' parameter of ``update`` or use **update_all()** instead.

If you want to insert or update just one document, there is a shortcut that help you with that. :py:func:`~djamo.collections.BaseCollection.save` allow you to insert a new document or update an already exists document. for example::

    new_student = Student(name="Aburame Shino", age=22)

    students = Students()
    students.save(new_student)  # save will use insert to put data in database

    new_student.age = 20

    students.save(new_student)  # save will use update to update the new_student age field


Making queries
--------------
After inserting some data in database you can access those data by making queries on related collection by using :py:func:`~djamo.collections.BaseCollection.find` and :py:func:`~djamo.collections.BaseCollection.find_one`.

Let's make it quick (we use Students collection and Student from above example)::

    students = Students()

    students.find({"age": 18})  # find all the students with age of 18
    students.find_one({"age": 18})  # select only first matched student

You can use `query operators <http://docs.mongodb.org/manual/reference/operator/>`_ of Mongodb for making advance queries
.. seealso:: For more information take a look at :py:class:`~djamo.collections.Collection`.

More ...
--------
Take a look at **Djamo** :doc:`api/index`
