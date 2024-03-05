# srandom.com
A site for the management of clear statuses for super-random enthusiasts of pop'n music.

## Installation
### Requirements
- [Python](https://www.python.org/)
- [MySQL](https://www.mysql.com/)
- [pipenv](https://github.com/pypa/pipenv)
- [direnv](https://github.com/direnv/direnv#install) (optional)

### Setup the development environment
```
pipenv install
```

### Configure environment variables
```shell
cp .env.sample .env
vi .env # edit it
```

### Start the database and application
```
pipenv run docker_up
```

### Run tests
```
pipenv run test
```

## Commands
Below is a list of Django's custom commands.

### Scraping
Fetch music information from the S-Random Difficulty Table and export it to a CSV file.

```
python manage.py scraping [--silent]
```

### Update music information
Import music information from a CSV file and update the database accordingly.

```
python manage.py update_music
```

### Data migration
Migrate all clear data from one user (source) to another user (destination).

Note: Clear data from the source user cannot be recovered after migration.

```
python manage.py data_migration <migration source username> <migration destination username>
```

### CSV export
Export clear data for premium users to CSV files.

Files are saved in `csv/export/<username>.csv`.

```
python manage.py export2csv
```

### Delete user account
Deactivate a specific user account and permanently delete its clear data.

Note: Once deleted, clear data cannot be recovered.

```
python manage.py delete_account <username>
```
