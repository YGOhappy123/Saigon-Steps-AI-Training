import base64
import requests
import weaviate
from weaviate.classes.query import MetadataQuery, Filter
from ultralytics import YOLO
from io import BytesIO
from PIL import Image

model = YOLO("src/model/shoe_detector.pt")


def ensure_rgb(image):
    """
    Convert an image to RGB if it has an alpha channel or palette.
    Transparent areas will be filled with white.
    """

    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        return background

    return image.convert("RGB")


def store_images(product_id, image_list):
    client = weaviate.connect_to_local()

    if client.is_ready():
        collection = client.collections.get(name="ProductImage")

        cropped_images = []
        for image_url in image_list:
            image = Image.open(BytesIO(requests.get(image_url).content))
            result = model.predict(source=image, conf=0.4, verbose=False)

            for box in result[0].boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                cropped = image.crop((x1, y1, x2, y2))
                cropped = ensure_rgb(cropped)

                buffer = BytesIO()
                cropped.save(buffer, format="JPEG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                cropped_images.append({"image": img_base64, "productId": product_id})

        collection.data.insert_many(cropped_images)
        print(f"✅ Store image vectors successfully for product ID: {product_id}")
        client.close()
    else:
        print("❌ Connection failed")
        client.close()


def image_search(image_bytes):
    client = weaviate.connect_to_local()

    if client.is_ready():
        collection = client.collections.get(name="ProductImage")

        query_img = Image.open(BytesIO(image_bytes))
        width, height = query_img.size
        result = model.predict(source=query_img, conf=0.4, verbose=False)

        detections = []
        for box in result[0].boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            cropped = query_img.crop((x1, y1, x2, y2))
            cropped = ensure_rgb(cropped)

            buffer = BytesIO()
            cropped.save(buffer, format="JPEG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            search_result = collection.query.near_image(
                near_image=img_base64,
                return_properties=["productId"],
                return_metadata=MetadataQuery(certainty=True),
                limit=10,
            )

            groups = {}
            for item in search_result.objects:
                pid = item.properties["productId"]
                certainty = item.metadata.certainty
                if pid not in groups or certainty > groups[pid]:
                    groups[pid] = certainty

            detections.append(
                {
                    "boundingBox": {
                        "x1": x1 / width,
                        "y1": y1 / height,
                        "x2": x2 / width,
                        "y2": y2 / height,
                    },
                    "products": sorted(groups.items(), key=lambda x: x[1], reverse=True)[:4],
                }
            )

        client.close()
        return detections
    else:
        print("❌ Connection failed")
        client.close()


def delete_images(product_id):
    client = weaviate.connect_to_local()

    if client.is_ready():
        collection = client.collections.get(name="ProductImage")

        collection.data.delete_many(where=Filter.by_property("productId").equal(product_id))
        print(f"✅ Deleted images for product ID: {product_id}")

        client.close()
    else:
        print("❌ Connection failed")
        client.close()
