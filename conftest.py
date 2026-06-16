# conftest.py
import os
import pytest


@pytest.fixture(autouse=False)
def project_root():
    """Return path to the project root."""
    return os.path.dirname(__file__)
