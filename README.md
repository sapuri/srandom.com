# srandom.com
A clear status management site for super-random enthusiasts of pop'n music

[![Build Status](https://travis-ci.com/sapuri/srandom.com.svg?token=xwpmsyc4SnBSSQnifEya&branch=master)](https://travis-ci.com/sapuri/srandom.com)
[![Updates](https://pyup.io/repos/github/sapuri/srandom.com/shield.svg)](https://pyup.io/repos/github/sapuri/srandom.com/)

## Environment
* Python 3.6 >=
* Django 2.0 >=
* MySQL 5.5 >=

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
