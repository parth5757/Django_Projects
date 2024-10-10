# In this test show yield use. (pytest have separate yield fixture. which are not here use.)

import pytest
@pytest.fixture
def yield_fixture():
    print("start Test Phase")
    yield 6
    print("End Test")

def test_example1(yield_fixture):
    print("run-example-1")  
    assert yield_fixture == 6