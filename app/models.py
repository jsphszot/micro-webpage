from app import db, login
from datetime import datetime
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash,
    )
from flask_login import UserMixin

class User(UserMixin, db.Model):
    # alternative for naming table
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pwd_hash = db.Column(db.String(128))
    # high-level view of the relationship between users and posts, 
    # normally defined on the "one" side
    # backref - defines name of field that will be added to the objects of the "many" class that points to "one" object
    posts = db.relationship('Post', backref='author', lazy='dynamic') 

    # tell python how to print objects of this class
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # in timestamp - function without call (), pass function itself
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.body}'

# keep track of logge in users by storing id in Flask's user session
# configure a user loader function that can be called to load a user given the ID
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# https://subscription.packtpub.com/book/web_development/9781784393656/7
# https://pythonbasics.org/flask-mongodb/
# better use mongo?
class Beers(db.Model):
    __tablename__ = 'beers'

    len_description = 300
    len_product = 64

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(len_product), index=True, unique=True)
    description = db.Column(db.String(len_description))
    alcohol = db.Column(db.Float)
    mls = db.Column(db.Integer)
    price = db.Column(db.Integer)
    available = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Beers {self.product}>'

class Pizzas(db.Model):
    __tablename__ = 'pizzas'

    len_description = 300
    len_product = 64

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(300))
    price = db.Column(db.Integer)
    available = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Pizzas {self.product}>'

    # BEERS
        # "name": "NEGRA STOUT",
        # "description": "nuestra cl&aacute;sica cerveza negra.",
        # "alcohol": "5,8",
        # "price": "$3.500",
        # "mls": 470,
        # "available": "Y"

    # PIZZAS
        # "name": "TAI MAN&Iacute;-&Aacute;TICO",
        # "description": "inspiraci&oacute;n tailandesa: salsa de maní + gengibre + ajo + merk&eacute;n + mozzarella + queso azul + longanicilla.",
        # "price": "$14.500",
        # "available": "Y"

    