import os
import sys
import pytest


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from djamo.base import Client
client = Client(config={"name": "djamo_test"})
client.drop_database()

pytest.main("--ignore=env -s %s" % (" ".join(sys.argv[1:])))
