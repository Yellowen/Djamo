import os
import sys
import pytest


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

pytest.main("--ignore=env")
