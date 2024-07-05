# import pytest
# # fixture
# # @pytest.fixture
# # def fixture_1(scope="session"):
# #     print('run-fixture-1')
# #     return 1

# # def test_example1(fixture_1):
# #     print("run-example-1")  
# #     num = fixture_1
# #     assert num == 1
    

# @pytest.fixture
# def yield_fixture():
#     print("start Test Phase")
#     yield 6
#     print("End Test")

# def test_example1(yield_fixture):
#     print("run-example-1")  
#     assert yield_fixture == 6