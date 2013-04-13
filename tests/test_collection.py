import time
import sys

from djamo.base import Client
from djamo import Collection, Document


class Student(Document):
    pass


class Students(Collection):
    document = Student


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

    def test_mass__insert(self):
        print("Massive insert------------------------")
        client = Client(config={"name": "djamo_test"})
        c = Students(client=client)

        start = time.time()
        l = list()
        append = l.append
        for i in xrange(200000):
            a = Student({"name": "Monkey .D Luffy%s" % i,
                         "ttl": i/2000})
            a.age = i
            append(a)

        c.insert(l)
        stop = time.time()
        print("MASS INSERT: %f" % (stop - start))

    def test_find(self):
        print("Find --------------")
        c = self.fixture()

        start = time.time()
        c.find({"name": "Monkey .D Luffy%s" % 960000})
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
