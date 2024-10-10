# old one
# import pytest

# # function    Run once per test
# # class       Run once per class of tests
# #module       Run once per module
# # session     Run once per session


# # # @pytest.mark.webtest
# # # @pytest.mark.skip
# # # @pytest.mark.xfail
# # # this three use for skip or ignore any test
# # def test_example():
# #     # here in commented code there is one pytest learning is that when we ise the wrong the before example it automatically detect and stop at there if you do this thing in next test than it stop at there 
# #     # print("hello")
# #     # assert 1 == 2
# #     assert 1 == 1

# def test_example1():
#     assert 1 == 1

import pytest

@pytest.fixture
def fixture_1():
    print('run-fixture-1')
    return 1

def test_example1(fixture_1):
    print('run-example-1')
    num = fixture_1
    assert num == 1