from flaskblog import db


if __name__ == '__main__':
    print("Dropping database...")
    db.drop_all()
    print("Done")

    print("Creating database...")
    db.create_all()
    print("Done")
