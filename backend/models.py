from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

# Chat model to store chat messages between the user and the chatbot
class Chat(db.Model):
    __tablename__ = "chats"  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key for each chat message
    role = db.Column(db.String(10), nullable=False)  # Role of the message sender (e.g., "user" or "bot")
    message = db.Column(db.Text, nullable=False)  # The chat message content
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp for message creation
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking the message to a user

    # Convert chat message details to a dictionary for serialization
    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }

# User model to represent users in the application
class User(db.Model):
    __tablename__ = "users"  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    name = db.Column(db.String(100))  # User's name
    email = db.Column(db.String(100))  # User's email address
    chats = db.relationship('Chat', backref='user', lazy=True)  # Relationship with the Chat model

    # Convert user details to a dictionary for serialization
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

# Products model to represent items available in the store
class Products(db.Model):
    __tablename__ = "products"  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the product
    name = db.Column(db.String(255), nullable=False)  # Product name
    brand = db.Column(db.String(100), nullable=False)  # Brand of the product
    category = db.Column(db.String(100), nullable=False)  # Category of the product
    price = db.Column(db.Float, nullable=False)  # Price of the product
    rating = db.Column(db.Float, nullable=False)  # Average rating of the product
    stock = db.Column(db.Integer, nullable=False)  # Stock availability
    description = db.Column(db.Text)  # Description of the product
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp for when the product was added

    # Convert product details to a dictionary for serialization
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "stock": self.stock,
            "description": self.description,
            "created_at": self.created_at,
        }

# Cart model to represent a user's shopping cart
class Cart(db.Model):
    __tablename__ = "carts"  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the cart
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Foreign key linking the cart to a user
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")  # Relationship with CartItem

    # Calculate the total price of all items in the cart
    def total_price(self):
        return sum([item.total_price() for item in self.items])

    # Convert cart details to a dictionary for serialization
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items],
            "total_price": self.total_price()
        }

# CartItem model to represent individual items in a cart
class CartItem(db.Model):
    __tablename__ = "cart_items"  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the cart item
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)  # Foreign key linking the item to a cart
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Foreign key linking the item to a product
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Quantity of the product in the cart

    product = db.relationship('Products', backref=db.backref('cart_items', lazy=True))  # Relationship with the Products model

    # Calculate the total price of the cart item (price * quantity)
    def total_price(self):
        return self.quantity * self.product.price

    # Convert cart item details to a dictionary for serialization
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name,
            "quantity": self.quantity,
            "total_price": self.total_price()
        }
