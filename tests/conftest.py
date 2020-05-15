import os

import pytest

# conftest.py > tests > simple-proxy
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


@pytest.fixture()
def test_data_dir():
    return os.path.join(BASE_DIR, "test_data")
