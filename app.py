from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

inventory = []
current_id = 1

# HOME ROUTE

@app.route('/')
def home():
    return "Inventory API is running"

# GET ALL ITEMS

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

# GET SINGLE ITEM

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

# ADD ITEM

@app.route('/inventory', methods=['POST'])
def add_item():
    global current_id
    data = request.json

    item = {
        "id": current_id,
        "name": data.get("name"),
        "quantity": data.get("quantity"),
        "price": data.get("price"),
        "barcode": data.get("barcode")
    }

    # OPTIONAL: enrich with API
    if item["barcode"]:
        product = fetch_from_api(barcode=item["barcode"])
        if product:
            item["product_data"] = product

    inventory.append(item)
    current_id += 1

    return jsonify(item), 201

# UPDATE ITEM

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.json
    item = next((i for i in inventory if i["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    item.update(data)
    return jsonify(item)

# Deleting items

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item deleted"})

# EXTERNAL API FUNCTION

def fetch_from_api(barcode=None, name=None):
    try:
        if barcode:
            url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        elif name:
            url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&search_simple=1&json=1"
        else:
            return None

        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()

        # handle product not found
        if data.get("status") == 0:
            return None

        return data

    except:
        return None

# EXTERNAL API ROUTE

@app.route('/external/product', methods=['GET'])
def get_external_product():
    barcode = request.args.get('barcode')
    name = request.args.get('name')

    if not barcode and not name:
        return jsonify({"error": "Provide barcode or name"}), 400

    data = fetch_from_api(barcode, name)

    if not data:
        return jsonify({"error": "Product not found or API failed"}), 404

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)