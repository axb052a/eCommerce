#!/usr/bin/env python3
import bcrypt
from models import User, Product, Order
# Standard library imports
from random import choice as rc, randint

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import *

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
    
        db.drop_all()
        db.create_all()
        
        # Seed for Users
        user_list = [
            {"username": "Anthony", "email": "anthony@example.com", "password": "password1"},
            {"username": "Jessica", "email": "jessica@example.com", "password": "password2"},
            {"username": "Kevin", "email": "kevin@example.com", "password": "password3"},
            {"username": "Ashley", "email": "ashley@example.com", "password": "password4"},
            {"username": "Charlie", "email": "charlie@example.com", "password": "password5"},
            {"username": "Donna", "email": "donna@example.com", "password": "password6"},
            {"username": "Michael", "email": "michael@example.com", "password": "password7"},
        ]

        for user_data in user_list:
            user = User(username=user_data["username"], email=user_data["email"])

            password = user_data["password"].encode("utf-8")
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            user._password_hash = password_hash
            db.session.add(user)
        db.session.commit()
        print("Users seeded successfully.")

        # Seed for Products
        products_list = [
            {"name": "Men's Slim Fit Shirt", "description": "Cotton-blend shirt with slim fit design", "price": 29.99},
            {"name": "Women's Skinny Jeans", "description": "High-rise skinny jeans with stretch fabric", "price": 49.99},
            {"name": "Men's Leather Belt", "description": "Genuine leather belt with silver-tone buckle", "price": 39.99},
            {"name": "Women's Knit Sweater", "description": "Cozy knit sweater with ribbed cuffs and hem", "price": 39.99},
            {"name": "Men's Classic Chinos", "description": "Cotton-blend chinos with classic fit", "price": 34.99},
            {"name": "Women's Faux Leather Jacket", "description": "Faux leather moto jacket with quilted detailing", "price": 59.99},
            {"name": "Men's Crew Neck T-shirt", "description": "Soft cotton crew neck t-shirt", "price": 19.99},
            {"name": "Women's Wrap Dress", "description": "Floral-print wrap dress with tie waist", "price": 44.99},
            {"name": "Men's Denim Jacket", "description": "Classic denim jacket with button front", "price": 49.99},
            {"name": "Women's Ankle Boots", "description": "Faux suede ankle boots with stacked heel", "price": 54.99},
            {"name": "Men's Hooded Sweatshirt", "description": "Fleece-lined hooded sweatshirt with kangaroo pocket", "price": 39.99},
            {"name": "Women's High-Waisted Shorts", "description": "High-waisted denim shorts with distressed detailing", "price": 29.99},
            {"name": "Men's Plaid Flannel Shirt", "description": "Brushed cotton plaid flannel shirt", "price": 34.99},
            {"name": "Women's Striped Sweater", "description": "Striped knit sweater with boat neckline", "price": 34.99},
            {"name": "Men's Cargo Shorts", "description": "Cargo shorts with multiple pockets and belt loops", "price": 24.99},
            {"name": "Women's Puffer Jacket", "description": "Quilted puffer jacket with hood and zip closure", "price": 69.99},
            {"name": "Men's V-Neck Sweater", "description": "Merino wool v-neck sweater with ribbed trim", "price": 49.99},
            {"name": "Women's Graphic T-shirt", "description": "Cotton-blend graphic print t-shirt", "price": 14.99},
            {"name": "Men's Sports Jacket", "description": "Lightweight sports jacket with zip front", "price": 59.99},
            {"name": "Women's Midi Skirt", "description": "A-line midi skirt with elastic waistband", "price": 29.99},
        ]

        for product_data in products_list:
            product = Product(name=product_data["name"], description=product_data["description"], price=product_data["price"])
            db.session.add(product)

        db.session.commit()
        print("Products seeded successfully.")
        
        # Seed for Orders
        users = User.query.all()
        products = Product.query.all()

        for _ in range(20):
            user = rc(users)
            product = rc(products)
            order = Order(
                user_id=user.id,
                product_id=product.id,
                quantity=randint(1, 5)
            )
            db.session.add(order)
        db.session.commit()
        print("Orders seeded successfully.")
