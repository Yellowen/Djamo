import time
import sys

from djamo.base import Client
from djamo import Collection, Document


class Student(Document):
    pass


class Students(Collection):
    document = Student


class TestCollectionInsert:

    def test_single_insert(self):
        client = Client(config={"name": "djamo_test"})
        c = Students(client=client)

        start = time.time()
        a = Student({"name": "Monkey .D Luffy"})
        a.age = 21
        c.insert(a)
        stop = time.time()
        print("\nINSERT: %f" % (stop - start))
