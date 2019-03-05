from flaskblog import db
from flaskblog.create_default_statuses import CreateDefaultStatuses


class DatabaseReset():
    def __init__(self):
        print('Dropping database...')
        db.drop_all()
        print('Done')

        print('Creating database...')
        db.create_all()
        print('Done')

        print('Setting up default statuses')
        service = CreateDefaultStatuses()
        service.create_default()
        print('Done')
