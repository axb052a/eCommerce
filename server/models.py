from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property  
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Serialization
    serialize_rules = ('-password_hash', '-user')

    @hybrid_property
    def password_hash(self):
        raise ValueError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    @validates('username', 'email')
    def validate_signup(self, key, value):
        if not (len(value) >= 3):
            raise ValueError("User or Email must provide at least three characters to sign up.")

        # Check if the username or email already exists
        existing_user = User.query.filter(db.or_(User.username == value, User.email == value)).first()
        if existing_user:
            raise ValueError(" User already exists.")

        return value

    def __repr__(self):
        return f"User {self.username}, ID {self.id}"

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product {self.name}, ID {self.id}"

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Define the relationship with the Product model
    product = db.relationship('Product', backref='orders')

    def __repr__(self):
        return f"Order ID: {self.id}, User ID: {self.user_id}"
    

