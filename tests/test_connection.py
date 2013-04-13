import sys
print(sys.path)
from djamo.base import Client


class TestConnection:

    def test_connect(self):
        c = Client(config={"name": "djamo_test"})
        c.terminate_connection()
