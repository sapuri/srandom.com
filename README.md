# srandom.com
A clear status management site for super-random enthusiasts of pop'n music

[![Build Status](https://travis-ci.com/sapuri/srandom.com.svg?token=xwpmsyc4SnBSSQnifEya&branch=master)](https://travis-ci.com/sapuri/srandom.com)

## Installation
### Requirements
- [Python](https://www.python.org/) 3.9 >=
- [Django](https://www.djangoproject.com/) 3.0 >=
- [MySQL](https://www.mysql.com/) 5.6 >=
- [direnv](https://github.com/direnv/direnv#install) (optional)

### Install dependent tools
```
pipenv install
```

### Set environment variables
```shell
cp .envrc_sample .envrc
direnv allow
```

### Create local_settings.py
```shell
cp srandom/local_settings_sample.py srandom/local_settings.py
vi srandom/local_settings.py
```

### Run test
```
python manage.py test
```

## Commands
A list of commands that use Django's command functions.

### Scraping
Obtain music information from the S-Random Difficulty Table and output it to a CSV file.

```
python manage.py scraping [--silent]
```

### Update music information
Read music information from CSV file and update database.

```
python manage.py update_music
```

### Data migration
All the clear data of the migration source user is migrated to the migration destination user.

The clear data of the migration source user cannot be restored.

```
python manage.py data_migration <migration source username> <migration destination username>
```

### CSV export
Output clear data of premium users as CSV files.

Output to `csv/export/<username>.csv`.

Usually run as cron.

```
python manage.py export2csv
```

### Delete user account
Disable the specified user account and delete the clear data completely.

Clear data cannot be restored.

```
python manage.py delete_account <username>
```
