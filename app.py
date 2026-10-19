# app.py - the Flask API (the "server")
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Our fake database: a plain list. Each item has an id.
inventory = [
    {
        "id": 1,
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar",
        },
        "price": 3.99,
        "stock": 20,
    },
    {
        "id": 2,
        "status": 1,
        "product": {
            "product_name": "Crunchy Peanut Butter",
            "brands": "Jif",
            "ingredients_text": "Roasted peanuts, sugar, salt",
        },
        "price": 4.50,
        "stock": 35,
    },
]

# The id the next new item will get
next_id = 3


def find_item(item_id):
    """Look through the list and return the item with this id (or None)."""
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def get_from_openfoodfacts(barcode, name):
    """Ask the OpenFoodFacts website for a product.
    Returns the product info, or None if nothing was found."""
    if barcode:
        url = "https://world.openfoodfacts.org/api/v2/product/" + barcode
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") == 1:
            return data["product"]
        return None

    url = "https://world.openfoodfacts.org/cgi/search.pl"
    options = {"search_terms": name, "search_simple": 1, "action": "process",
               "json": 1, "page_size": 1}
    response = requests.get(url, params=options, timeout=10)
    products = response.json()["products"]
    if len(products) == 0:
        return None
    return products[0]


# ---------- CRUD routes ----------

# READ: get all items
@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200


# READ: get one item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_one_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


# CREATE: add a new item
@app.route("/inventory", methods=["POST"])
def add_item():
    global next_id
    data = request.get_json()

    if data is None or "product_name" not in data:
        return jsonify({"error": "product_name is required"}), 400

    try:
        price = float(data["price"])
        stock = int(data["stock"])
    except (KeyError, ValueError):
        return jsonify({"error": "price and stock must be numbers"}), 400

    new_item = {
        "id": next_id,
        "status": 1,
        "product": {
            "product_name": data["product_name"],
            "brands": data.get("brands", ""),
            "ingredients_text": data.get("ingredients_text", ""),
        },
        "price": price,
        "stock": stock,
    }
    inventory.append(new_item)
    next_id = next_id + 1
    return jsonify(new_item), 201


# UPDATE: change price and/or stock
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "No data sent"}), 400

    try:
        if "price" in data:
            item["price"] = float(data["price"])
        if "stock" in data:
            item["stock"] = int(data["stock"])
    except ValueError:
        return jsonify({"error": "price and stock must be numbers"}), 400

    return jsonify(item), 200


# DELETE: remove an item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify({"message": "Item deleted"}), 200


# ---------- Extra routes that use the OpenFoodFacts API ----------

# Search OpenFoodFacts (does not save anything)
# Example: /lookup?barcode=3017620422003   or   /lookup?name=nutella
@app.route("/lookup", methods=["GET"])
def lookup():
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    if not barcode and not name:
        return jsonify({"error": "Give a barcode or a name"}), 400

    try:
        product = get_from_openfoodfacts(barcode, name)
    except requests.exceptions.RequestException:
        return jsonify({"error": "OpenFoodFacts is not responding"}), 502

    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"status": 1, "product": product}), 200


# Search OpenFoodFacts AND add the result to our inventory
@app.route("/inventory/from-api", methods=["POST"])
def add_from_api():
    global next_id
    data = request.get_json()
    if data is None or not (data.get("barcode") or data.get("name")):
        return jsonify({"error": "Give a barcode or a name"}), 400

    try:
        price = float(data["price"])
        stock = int(data["stock"])
    except (KeyError, ValueError):
        return jsonify({"error": "price and stock must be numbers"}), 400

    try:
        product = get_from_openfoodfacts(data.get("barcode"), data.get("name"))
    except requests.exceptions.RequestException:
        return jsonify({"error": "OpenFoodFacts is not responding"}), 502

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    new_item = {
        "id": next_id,
        "status": 1,
        "product": {
            "product_name": product.get("product_name", "Unknown"),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
        },
        "price": price,
        "stock": stock,
    }
    inventory.append(new_item)
    next_id = next_id + 1
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)