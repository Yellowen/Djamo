from djamo.base import Client
from djamo import Collection, Document
from djamo.serializers import *


class Car(Document):
    fields = {
        "model": String(min_length=3, max_length=15, required=True),
        "cost": Float(min=0.0, max=40000.50),
        "owners": List(),
        "acc": Integer(min=30, max=60),
    }


class Cars(Collection):
    document = Car


class TestSerializers:

    def fixture(self):
        client = Client(config={"name": "djamo_test"})
        c = Cars(client=client)
        return c

    def test_serializer(self):
        print("\nSerializers test --------------")
        c = self.fixture()

        a = Car({"model": "Some Long string that pass tha mx value",
                  "cost": 300000000,
                  "owner": [1, 2, 3, 4],
                  "acc": 70})

        c.insert(a)
