# old code
# import pytest

# from django.contrib.auth.models import User

# @pytest.mark.django_db
# def test_user_create():
#     User.objects.create_user('test', 'test@example.in', 'test')
#     count = User.objects.all().count()
#     print(count)
#     assert User.objects.count() == 1


# @pytest.mark.django_db
# def test_user_create1():
#     count = User.objects.all().count()
#     print(count)
#     assert count == 0


# def test_set_check_password(user_1):
#     print('check-user1')
#     assert user_1.username == "test-user"

# def test_set_check_password2(user_1):
#     print('check-user2')
#     assert user_1.username == "test-user"


import pytest

from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('test', 'test@test.com')
    assert User.objects.count() == 1