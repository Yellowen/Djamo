import pytest

from djamo.base import Client
from djamo import Collection, Document
from djamo.serializers import *


class Car(Document):
    fields = {
        "model": String(min_length=3, max_length=15, required=True),
        "cost": Float(min_value=7.0, max_value=40000.50),
        "owners": List(),
        "acc": Integer(min_value=30, max_value=60),
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

        a = Car({"model": "sdfsdfasdfasdfasdfasdfasdfasdfasdfasgf"})
        b = Car()

        c.insert(b)

        with pytest.raises(String.ValidationError):
            c.insert(a)
