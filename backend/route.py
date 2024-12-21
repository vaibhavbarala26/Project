from flask import Flask, request, jsonify
from config import app, db
from models import User, Cart, CartItem, Products , Chat
from werkzeug.exceptions import BadRequest

# Route for user registration
@app.route("/auth", methods=["POST"])
def register():
    try:
        # Parse request JSON data
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
      
        # Validate required fields
        if not name or not email :
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if the user already exists
        found = User.query.filter_by(email=email).first()
        if found:
           return jsonify({"message":"Login successfull"}),200
        
        # Create a new user and save to the database
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to add a single product
@app.route("/product", methods=["POST"])
def add_product():
    try:
        # Parse request JSON data
        data = request.get_json()

        # Extract product details
        name = data.get("name")
        brand = data.get("brand")
        category = data.get("category")
        price = data.get("price")
        rating = data.get("rating")
        stock = data.get("stock")
        description = data.get("description")

        # Validate required fields
        if not name or not brand or not category or not price or not rating or not stock:
            raise BadRequest("Missing required fields")

        # Create a new product and save to the database
        new_product = Products(
            name=name,
            brand=brand,
            category=category,
            price=price,
            rating=rating,
            stock=stock,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        # Return success response with product details
        return jsonify({
            "message": "Product added successfully",
            "product": new_product.to_dict()
        }), 201
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Route to add multiple products at once
@app.route('/add-products', methods=['POST'])
def add_products():
    try:
        # Parse request JSON data
        products = request.get_json()
        
        # Ensure input is a list of products
        if not isinstance(products, list):
            return jsonify({"error": "Expected a list of products"}), 400

        # Create Product objects and save them to the database
        product_objects = [
            Products(
                name=product['name'],
                brand=product['brand'],
                category=product['category'],
                price=product['price'],
                stock=product['stock'],
                rating=product['rating'],
                description=product['description']
            )
            for product in products
        ]
        db.session.bulk_save_objects(product_objects)
        db.session.commit()

        return jsonify({"message": "Products added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to search for products with various filters
@app.route("/get-product", methods=["GET"])
def search():
    try:
        # Extract query parameters
        category = request.args.get("category")
        max_price = request.args.get("max_price", type=float)
        min_price = request.args.get("min_price", type=float)
        instock = request.args.get("instock", type=bool)
        brand = request.args.get("brand")
        name = request.args.get("name")
        rating = request.args.get("rating", type=float)
        limit = request.args.get("limit" , type=int)

        # Start building the querytype
        query = Products.query

        # Apply filters based on the provided query parameters
        if category:
            query = query.filter(Products.category.ilike(f"%{category}%"))
        if max_price is not None:
            query = query.filter(Products.price <= max_price)
        if min_price is not None:
            query = query.filter(Products.price >= min_price)
        if brand:
            query = query.filter(Products.brand.ilike(f"%{brand}%"))
        if name:
            query = query.filter(Products.name.ilike(f"%{name}%"))
        if rating is not None:
            query = query.filter(Products.rating >= rating)
        if instock is not None:
            query = query.filter(Products.stock >=1)

        # Fetch the filtered products
        query = query.limit(limit)
        products = query.all()

        # Convert results to JSON format
        products_list = [product.to_dict() for product in products]

        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-a-product" , methods=["GET"])
def get():
    product_id = request.args.get("id")

    if not product_id:
        return jsonify({"message":"error"}),500
    Product_found = Products.query.filter_by(id=product_id).first()
    prosuct = Product_found.to_dict()
    print(prosuct)
    return jsonify({"product": prosuct})
# Route to add items to the cart
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    try:
        # Parse request JSON data
        data = request.get_json()
        email = data.get("email")
        product = data.get("product")
        quantity = data.get("quantity", 1)

        # Validate user and product existence
        user_found = User.query.filter_by(email=email).first()
        product_found = Products.query.filter_by(id=product).first()
        if not product_found:
            return jsonify({"message": "Product not found"}), 404
        if not user_found:
            return jsonify({"message": "User not found"}), 404

        # Get or create a cart for the user
        cart = Cart.query.filter_by(user_id=user_found.id).first()
        if not cart:
            cart = Cart(user_id=user_found.id)
            db.session.add(cart)
            db.session.commit()

        # Get or create a cart item
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_found.id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_found.id, quantity=quantity)
            db.session.add(cart_item)

        # Save changes to the database
        db.session.commit()

        return jsonify({"message": "Item added to cart", "cart": cart.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/save-chat" , methods=["POST"])
def save():
    data = request.get_json()
    role = data.get("role")
    message = data.get("message")
    user_email = data.get("email")
    print(data)
    user_found = User.query.filter_by(email=user_email).first()
    if not user_found or not role or not message:
        return jsonify({"message":"error"}),500
    
    chat = Chat(role=role , user_id = user_found.id , message=message )
    db.session.add(chat)
    db.session.commit()
    return jsonify(chat.to_dict()),201
@app.route("/get-chat", methods=["GET"])
def get_chat():
    try:
        # Get email from query parameters
        user_email = request.args.get("email")
        if not user_email:
            return jsonify({"error": "Email is required"}), 400

        # Find the user by email
        user_found = User.query.filter_by(email=user_email).first()
        if not user_found:
            return jsonify({"error": "User not found"}), 404

        # Retrieve all chats for the user
        chats = Chat.query.filter_by(user_id=user_found.id).order_by(Chat.created_at).all()
        if not chats:
            return jsonify({"message": "No chats found for this user"}), 404

        # Serialize the chats into JSON format
        chat_list = [chat.to_dict() for chat in chats]
        return jsonify({"user": user_found.to_dict(), "chats": chat_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/cart", methods=["GET"])
def get_cart():
    try:
        # Get the email from query parameters
        email = request.args.get("email")
        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Find the user by email
        found_user = User.query.filter_by(email=email).first()
        if not found_user:
            return jsonify({"error": "User not found"}), 404

        # Retrieve the cart for the user
        cart_items = Cart.query.filter_by(user_id=found_user.id).all()
        if not cart_items:
            return jsonify({"message": "No items found in the cart"}), 404

        # Serialize the cart items into JSON format
        cart_data = [item.to_dict() for item in cart_items]
        return jsonify({"message": "Cart found", "cart": cart_data}), 200

    except Exception as e:
        # Return error message with status code 500 for server errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables for the primary database
    app.run(debug=True)
