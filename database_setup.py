from flaskblog import db
from flaskblog.create_default_statuses import CreateDefaultStatuses


if __name__ == '__main__':
    print('Dropping database...')
    db.drop_all()
    print('Done')

    print('Creating database...')
    db.create_all()
    print('Done')

    print('Setting up default statuses')
    # CreateDefaultStatuses.perform()
    service = CreateDefaultStatuses()
    service.create_default()
