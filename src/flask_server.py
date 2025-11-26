from flask import Flask, jsonify, request
from flask_cors import CORS
from create_collections import recreate_collections
from image_search import image_search, store_images, delete_images
from semantic_search import semantic_search, store_description, delete_description
from similar_search import get_similar_products

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello World From PTIT HCM!'}), 200


@app.route('/recreate-collections', methods=['POST'])
def recreate_collections_controller():
    recreate_collections()

    return jsonify({'message': 'Products seeded successfully'}), 200


@app.route('/add-product', methods=['POST'])
def add_product_controller():
    if request.is_json:
        body = request.get_json()

        product_id = body.get('rootProductId')
        image_list = body.get('images', [])
        name = body.get('name', '')
        price = body.get('price', 0)
        brand = body.get('brand', '')
        sizes = body.get('sizes', [])
        features = body.get('shoeFeature', {})
        store_images(product_id, image_list)
        store_description(product_id, name, price, brand, sizes, features)

        return jsonify({'message': 'Product added successfully'}), 201
    else:
        return jsonify({'message': 'Request must be JSON'}), 422


@app.route('/update-product/<int:product_id>', methods=['PATCH'])
def update_product_controller(product_id):
    if request.is_json:
        body = request.get_json()

        image_list = body.get('images', [])
        name = body.get('name', '')
        price = body.get('price', 0)
        brand = body.get('brand', '')
        sizes = body.get('sizes', [])
        features = body.get('shoeFeature', {})
        delete_images(product_id)
        delete_description(product_id)
        store_images(product_id, image_list)
        store_description(product_id, name, price, brand, sizes, features)

        return jsonify({'message': 'Product updated successfully'}), 200
    else:
        return jsonify({'message': 'Request must be JSON'}), 422


@app.route('/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product_controller(product_id):
    delete_images(product_id)
    delete_description(product_id)

    return jsonify({'message': 'Product deleted successfully'}), 200


@app.route('/image-search', methods=['POST'])
def image_search_controller():
    if 'image' in request.files:
        image_file = request.files['image']
        image_bytes = image_file.read()
        detections = image_search(image_bytes)

        return jsonify({'data': {"detections": detections}}), 200
    else:
        return jsonify({'message': 'No image file provided'}), 400


@app.route('/semantic-search', methods=['POST'])
def semantic_search_controller():
    if request.is_json:
        body = request.get_json()
        query = body.get('query', '')
        detections = semantic_search(query)

        return jsonify({'data': {"detections": detections}}), 200
    else:
        return jsonify({'message': 'Request must be JSON'}), 422


@app.route('/similar-products/<int:product_id>', methods=['GET'])
def get_similar_products_controller(product_id):
    detections = get_similar_products(product_id)

    return jsonify({'data': {"detections": detections}}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
