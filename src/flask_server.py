from flask import Flask, jsonify, request
from image_search import store_images, image_search

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello World From PTIT HCM!'}), 200


@app.route('/store-products', methods=['POST'])
def store_products_controller():
    if request.is_json:
        data = request.get_json()
        for product in data.get('products', []):
            product_id = product.get('rootProductId')
            image_list = product.get('images', [])
            store_images(product_id, image_list)
            print(f"Stored images for product ID: {product_id}")

        return jsonify({'message': 'Products stored successfully'}), 201
    else:
        return jsonify({'message': 'Request must be JSON'}), 422


@app.route('/image-search', methods=['POST'])
def image_search_controller():
    if 'image' in request.files:
        image_file = request.files['image']
        image_bytes = image_file.read()
        detections = image_search(image_bytes)

        return jsonify({'data': {"detections": detections}}), 200
    else:
        return jsonify({'message': 'No image file provided'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
