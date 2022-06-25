import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def setup_db(app):
    database_name ='bookrecomm'
    default_database_path= "postgres://{}:{}@{}/{}".format(
        'postgres', 'password', 'localhost:5432', database_name
    )
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


"""
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
"""


class Buy(db.Model):
    __tablename__ = 'bookbuys'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    book_id = Column(Integer)

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id

    def details(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    name = Column(String(1024))
    price = Column(Integer)
    status = Column(String(32))
    author = Column(String(1024))
    publisher = Column(String(1024))
    description = Column(String(8192))
    category_id = Column(Integer)
    created_at_timestamp = Column(Integer)
    buy_count = Column(Integer)

    def __init__(
        self, book_id, name, price, status, author, publisher, description, category_id, created_at, buy_count
    ):
        self.book_id = book_id
        self.name = name
        self.price = price
        self.status = status
        self.author = author
        self.publisher = publisher
        self.description = description
        self.category_id = category_id
        self.created_at = created_at
        self.buy_count = buy_count

    def details(self):
        return {
            'id': self.id,
            "book_id": self.book_id,
            "name": self.name,
            "price": self.price,
            "status": self.status,
            "author": self.author,
            "publisher": self.publisher,
            "description": self.description,
            "category_id": self.category_id,
            "created_at": self.created_at,
            "buy_count": self.buy_count,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
