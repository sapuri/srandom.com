# srandom.com
A clear status management site for super-random enthusiasts of pop'n music

## Installation
### Requirements
- [Python](https://www.python.org/)
- [MySQL](https://www.mysql.com/)
- [pipenv](https://github.com/pypa/pipenv)
- [direnv](https://github.com/direnv/direnv#install) (optional)

### Create development environment
```
pipenv install
```

### Set environment variables
```shell
cp .env.sample .env
vi .env # edit it
```

### Start DB and app
```
pipenv run docker_up
```

### Run test
```
pipenv run test
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
