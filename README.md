## KU Polls: Online Survey Questions 

[![Unittest for views and models](https://github.com/0CreepySmile0/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/0CreepySmile0/ku-polls/actions/workflows/django.yml)
[![Flake8 on models and views](https://github.com/0CreepySmile0/ku-polls/actions/workflows/flake8_test.yml/badge.svg)](https://github.com/0CreepySmile0/ku-polls/actions/workflows/flake8_test.yml)

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation

See [full instruction](Installation.md)

## Running the Application

Follow the installation instruction before running the server.
Note: to run the command, you must be in the cloned directory.
```shell
python manage.py runserver
```
Or try this if background image not load or the appearance is broken
```shell
python manage.py runser --insecure
```
When you want to terminate app press `Ctrl-C`<br>
To exit virtual environment. Simply run this
```shell
deactivate
```

## User in data fixture
Here is username and password from data fixture

|Username|Password|Super user?|
|:--|:--|:--|
|admin|admin1234|Yes|
|demo1|hackme11|No|
|demo2|hackme22|No|
|demo3|hackme33|No|

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Domain Model](../../wiki/Domain%20Model)
- [Iteration Plan](../../wiki#iteration-plan)
