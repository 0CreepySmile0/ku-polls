## Requirements
- Python version 3.11 installed on your device. If not, see [how to install python](https://pythontutorial.net/getting-started/install-python). (Again, select Python 3.11)
- Git command is installed. If not, see [how to install git](https://github.com/git-guides/install-git).

## Cloning or downloading from GitHub
Clone the repository to your local device using the following command in terminal.
```shell
git clone https://github.com/0CreepySmile0/ku-polls.git
```

## Create virtual environment and install dependencies
First, you will have to navigate to the cloned repository first.
```shell
cd ku-polls
```
Make sure you have `virtualenv` python package installed first.
```shell
pip install virtualenv
```
And then activate virtualenv.
```shell
virtualenv env
```
Linux and MacOS use
```shell
. env/bin/activate
```
Window use
```shell
env\Scripts\activate
```
Install required packages.
```shell
pip install -r requirements.txt
```

## Set environment variables
First, you will need to generate some random secret key using shell.
```shell
python manage.py shell
```
Import random key generator.
```py
from django.core.management.utils import get_random_secret_key
```
Get random key and copy the output.
```py
get_random_secret_key()
```
Exit from python shell.
```py
exit()
```
Now you will need to create `.env` file and set variable for the app by using these command.
```shell
echo SECRET_KEY={copied-secret-key-without-quote}> .env
```
```shell
echo DEBUG=False>> .env
```
```shell
echo ALLOWED_HOSTS=localhost,127.0.0.1>> .env
```
For your time zone see [list of time zone.](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)<br>
Note: Use "TZ identifier" column.
```shell
echo TIME_ZONE={your-time-zone}>> .env
```

## Run migration and install data from data fixture
To run migration, use the following command.
```shell
python manage.py migrate
```
Install data from fixture.
```shell
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```

## Run test
```shell
python manage.py test
```

## Running the Application
You have to do all above before doing this. If you have done all of them see [how to run.](README.md#running-the-application)
