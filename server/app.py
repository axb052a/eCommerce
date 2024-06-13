# Remote library imports
from flask import request, make_response, session, jsonify
from flask_restful import Resource
from werkzeug.exceptions import Unauthorized
import re

# Local imports
from config import app, db, api

# Add your model imports
from models import User, Product, Order

class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        # Check if all required data are present
        if not (username and email and password and password_confirmation):
            return {"error": "All data are required"}, 400

        # Check if password and confirmation match
        if password != password_confirmation:
            return {"error": "Password and confirmation do not match"}, 400

        new_user = User(username=username, email=email)

        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        return new_user.to_dict()

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Check if username and password are present
        if not (username and password):
            return {"error": "Username and password are required"}, 400

        user = User.query.filter(User.username == username).first()

        # Check if user exists
        if user:
            # Check if the password is correct
            if user.authenticate(password):
                session["user_id"] = user.id
                print(f"Debug: User ID set in session: {session['user_id']}")
                return user.to_dict(rules=("_password_hash",))
            else:
                return {"error": "Invalid username or password"}, 401
        else:
            return {"error": "User not found"}, 401

class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        print(f"Debug: User ID from session: {user_id}")

        if not user_id:
            print("Debug: No user in session")
            return {"message": "No user in session"}, 401

        user = User.query.get(user_id)

        if user:
            print(f"Debug: User found in the database - {user}")
            return user.to_dict(rules=("_password_hash",))
        else:
            print("Debug: User not found in the database")
            return {"message": "User not found in the database"}, 401

class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return {"message": "200: No Content"}, 200
    
class ProductResource(Resource):
    def get(self, product_id):
        try:
            product = Product.query.get(product_id)
            if product:
                return product.to_dict(), 200
            else:
                return {"message": "Product not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        new_product = Product(name=data.get("name"), description=data.get("description"), price=data.get("price"))

        try:
            db.session.add(new_product)
            db.session.commit()
            return new_product.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def put(self, product_id):
        data = request.get_json()
        product = Product.query.get(product_id)

        if not product:
            return {"message": "Product not found"}, 404

        product.name = data.get("name")
        product.description = data.get("description")
        product.price = data.get("price")

        try:
            db.session.commit()
            return product.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def delete(self, product_id):
        product = Product.query.get(product_id)

        if not product:
            return {"message": "Product not found"}, 404

        try:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class OrderResource(Resource):
    def get(self, order_id):
        try:
            order = Order.query.get(order_id)
            if order:
                return order.to_dict(), 200
            else:
                return {"message": "Order not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        new_order = Order(user_id=data.get("user_id"), product_id=data.get("product_id"), quantity=data.get("quantity"))

        try:
            db.session.add(new_order)
            db.session.commit()
            return new_order.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def put(self, order_id):
        data = request.get_json()
        order = Order.query.get(order_id)

        if not order:
            return {"message": "Order not found"}, 404

        order.user_id = data.get("user_id")
        order.product_id = data.get("product_id")
        order.quantity = data.get("quantity")

        try:
            db.session.commit()
            return order.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def delete(self, order_id):
        order = Order.query.get(order_id)

        if not order:
            return {"message": "Order not found"}, 404

        try:
            db.session.delete(order)
            db.session.commit()
            return {"message": "Order deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
# Cart management
class AddToCart(Resource):
    def post(self):
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        
        # Retrieve or create the user's cart from the session
        cart = session.get("cart", {})
        
        # Add the product to the cart or update its quantity if already exists
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        
        # Update the cart in the session
        session["cart"] = cart
        
        return jsonify({"message": "Product added to cart successfully"}), 200

class RemoveFromCart(Resource):
    def delete(self, product_id):
        # Retrieve the user's cart from the session
        cart = session.get("cart", {})
        
        # Remove the product from the cart if exists
        if product_id in cart:
            del cart[product_id]
        
        # Update the cart in the session
        session["cart"] = cart
        
        return jsonify({"message": "Product removed from cart successfully"}), 200

class UpdateCart(Resource):
    def put(self):
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        
        # Retrieve the user's cart from the session
        cart = session.get("cart", {})
        
        # Update the quantity of the product in the cart
        if product_id in cart:
            cart[product_id] = quantity
        
        # Update the cart in the session
        session["cart"] = cart
        
        return jsonify({"message": "Cart updated successfully"}), 200

# Checkout and payment processing
class Checkout(Resource):
    def post(self):
        # Retrieve the user's cart from the session
        cart = session.get("cart", {})
        
        # Logic to process the checkout and payment
        # Calculate total price based on the items in the cart
        
        # Clear the cart after successful checkout
        session["cart"] = {}
        
        return jsonify({"message": "Checkout successful"}), 200

# Add routes to the API
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")
api.add_resource(ProductResource, "/products/<int:product_id>")
api.add_resource(OrderResource, "/orders/<int:order_id>")
api.add_resource(AddToCart, "/add_to_cart")
api.add_resource(RemoveFromCart, "/remove_from_cart/<int:product_id>")
api.add_resource(UpdateCart, "/update_cart")
api.add_resource(Checkout, "/checkout")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
