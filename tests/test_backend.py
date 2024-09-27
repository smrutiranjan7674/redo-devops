import pytest
from backend import app

<p>@pytest.fixture
def client():
    return app.test_client()</p>
