from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock Database
inventory = [
    {"id": 1, "name": "Coffee Beans", "quantity": 50, "barcode": "00123"},
    {"id": 2, "name": "Oat Milk", "quantity": 20, "barcode": "00456"}
]

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing item data"}), 400
    
    new_item = {
        "id": len(inventory) + 1,
        "name": data['name'],
        "quantity": data.get('quantity', 0),
        "barcode": data.get('barcode', "")
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    inventory = [item for item in inventory if item['id'] != item_id]
    return '', 204

@app.route('/fetch-product/<barcode>', methods=['GET'])
def fetch_external_product(barcode):
    # Integration with Open Food Facts API
    url = f"https://world.openfoodfacts.org{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 1:
            product = data['product']
            return jsonify({
                "name": product.get('product_name', 'Unknown'),
                "brand": product.get('brands', 'Unknown')
            })
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
