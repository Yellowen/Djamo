import time
import sys

from djamo.base import Client
from djamo import Collection, Document, Index
from djamo.serializers import *


class Student(Document):
    pass


class Students(Collection):
    document = Student


class IStudents(Collection):
    document = Student
    indexes = [
        Index("age"),
    ]


class TestCollection:

    def fixture(self):
        client = Client(config={"name": "djamo_test"})
        c = Students(client=client)
        return c

    def test_single_insert(self):
        print("\nSingle Insert---------------------")
        client = Client(config={"name": "djamo_test"})
        c = Students(client=client)

        start = time.time()
        a = Student({"name": "Monkey .D Luffy"})
        a.age = 21
        c.insert(a)
        stop = time.time()
        print("INSERT: %f" % (stop - start))

    def test_mass_insert(self):
        print("Massive insert------------------------")
        client = Client(config={"name": "djamo_test"})
        c = Students(client=client)

        def wrap(i):
            a = Student({"name": "Monkey .D Luffy%s" % i,
                         "ttl": i/2000})
            a.age = a.ttl * 4
            return a

        l = [wrap(i) for i in range(200000)]

        print("Starting insert")
        start = time.time()
        c.insert(l)
        stop = time.time()
        print("MASS INSERT: %f" % (stop - start))

    def test_find(self):
        print("Find --------------")
        c = self.fixture()

        start = time.time()
        c.find({"age": 12})
        stop = time.time()
        print("FIND: %f" % (stop - start))

    def test_get_all(self):
        print("Find All --------------")
        c = self.fixture()

        start = time.time()
        d = c.find()
        stop = time.time()
        print("Count: ", d.count())
        print("FIND ALL: %f" % (stop - start))

    def test_update(self):
        print("Update --------------")
        c = self.fixture()

        start = time.time()
        c.update({"ttl": 3}, {"$set": {"name": "sameer"}})
        stop = time.time()
        d = c.find({"name": "sameer"}).count()
        print("updated %s" % d)
        print("UPDATE: %f" % (stop - start))

    def test_update_all(self):
        print("Update all --------------")
        c = self.fixture()

        start = time.time()
        c.update_all({"ttl": 3}, {"$set": {"name": "sameer"}})
        stop = time.time()
        d = c.find({"name": "sameer"}).count()
        print("updated %s" % d)
        print("UPDATE ALL: %f" % (stop - start))

    def test_remove(self):
        print("Remove --------------")
        c = self.fixture()

        start = time.time()
        c.remove({"ttl": 3})
        stop = time.time()
        d = c.find({"ttl": 3}).count()
        print("find %s" % d)
        print("Remove: %f" % (stop - start))

    def test_save(self):
        print("Save --------------")
        c = self.fixture()

        a = Student({"name": "narto", "age": 20})

        start1 = time.time()
        c.save(a)
        stop1 = time.time()

        a.name = "itachi"
        start2 = time.time()
        c.save(a)
        stop2 = time.time()

        print("Save: %f" % (stop1 - start1))
        print("Second Save: %f" % (stop2 - start2))

    def test_indexing(self):
        print("Indexing --------------")
        client = Client(config={"name": "djamo_test"})
        c = IStudents(client=client)

        def wrap(i):
            a = Student({"name": "Madara %s" % i,
                         "ttl": i/2000})
            a.age = a.ttl * 4
            return a
        l = [wrap(i) for i in range(200000)]

        print("Starting insert %s " % len(l))
        start = time.time()
        c.insert(l)
        stop = time.time()
        print("MASS INSERT WITH INDEX: %f" % (stop - start))

        start = time.time()
        d = c.find({"age": 12}).count()
        stop = time.time()
        print("%s found" % d)
        print("FIND WITH INDEX: %f" % (stop - start))
