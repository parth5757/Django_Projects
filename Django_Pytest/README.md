# Django Pytest

This is Documentation for django_pytest

Some other pytest framework which can also used.
- Robot, Unittest, DocTest, Nose2, Testify


Why choose to pytest

- PyTest is open source 
- work with built in units
- Easy to start and simple syntax
- is highly extensible using plugins
- support fixtures

What you know from here
- test folder structure
- Pytest Discovery
- Runing Test
    - Understand Test output
    - Report option
    - Specifying test run
    - Use Pytest Mark

# Pytest Documentation
=========================

## Installation

* `pip install Django`
* `pip install pytest-django`
* Create a new Django project with `django-admin startproject project_name .`
* Create a new Django app with `python manage.py startapp app_name`
* Create a `tests` folder inside the app and add a `test.py` file
* Create another `tests` folder in the main project folder with a `test_ex1.py` file
* Create a `pytest.ini` file for pytest settings

## Why Choose Pytest?

* Pytest is open source
* Works with built-in units
* Easy to start and simple syntax
* Highly extensible using plugins
* Supports fixtures

## What You Know So Far

* Test folder structure
* Pytest Discovery
* Running Tests
	+ Understanding Test Output
	+ Report Options
	+ Specifying Test Run
	+ Using Pytest Mark

## Pytest Fixtures
=====================

### Arrange, Act, Assert

* **Arrange**: Set up the test environment, including any necessary settings, objects, database connections, API connections, or web app connections.
* **Act**: Perform the action being tested, such as calling a function or API.
* **Assert**: Verify that the outcome of the action is correct.

### What is a Pytest Fixture?

* A function that runs before/after each test function to which it is applied (runs before the Act action)
* Used to feed data to the test, such as database connection URLs or input data

* fixture are applied in arrange phase
* fixtures are function
* Run before/after each test function to which the fixture is applied

why Pytest fixtures are used
- Fixtures are used to feed data to the tests such as database connections, URLs to test and input data.



### Fixture Scopes

* `function`: Run once per test
* `class`: Run once per class of tests
* `module`: Run once per module
* `session`: Run once per session

## Running Pytest
=====================

* `pytest -s`: Run pytest with output
* `pytest`: Simply run pytest
* `pytest -rP`: Run pytest with Django models


