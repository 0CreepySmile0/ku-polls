## Requirements
- Python version 3.11 installed on your device. If not, see [how to install python](https://pythontutorial.net/getting-started/install-python). (Again, select Python 3.11)
- Git command is installed. If not, see [how to install git](https://github.com/git-guides/install-git).

## Cloning or downloading from Github
Clone the repository to your local device using the following command in terminal.
```
git clone https://github.com/0CreepySmile0/ku-polls
```

## Create virtual environment and install dependencies
First, you will have to navigate to the cloned repository first.
```
cd ku-polls
```
Make sure you have `virtualenv` python package installed first.
```
pip install virtualenv
```
And then activate virtualenv.
```
virtualenv env

# Linux and MacOS
source env/bin/activate

# Window
env\Scripts\activate
```
Install required packages.
```
pip install -r requirements.txt
```

## Run migration and install data from data fixture
To run migration, use the following command.
```
python manage.py migrate
```
Install data from fixture.
```
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```

## Run test
```
python manage.py test
```
