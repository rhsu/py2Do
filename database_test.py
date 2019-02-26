from flaskblog import db, User, Post
from pdb import set_trace


def do_something():
    print("Creating users")
    user_1 = User(
        username='test',
        email='test@gmail.com',
        password='password'
    )

    user_2 = User(
        username='test2',
        email='test2@gmail.com',
        password='anotherpassword'
    )

    db.session.add(user_1)
    db.session.add(user_2)

    db.session.commit()

    print("Done")

    post_1 = Post(
        title='my first post',
        content='some content',
        user_id=user_1.id
    )

    db.session.add(post_1)
    db.session.commit()
    set_trace()


if __name__ == '__main__':
    print("Dropping database...")
    db.drop_all()
    print("Done")

    print("Creating database...")
    db.create_all()
    print("Done")
