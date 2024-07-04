import pytest


# providing access of database to test the data and many more
pytestmaek = pytest.mark.django_db

class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # ACt
        x = category_factory()
        # Assert 
        assert x.__str__() == "test_category"


class TestBrandModel:
    pass

class TestProductModel:
    pass