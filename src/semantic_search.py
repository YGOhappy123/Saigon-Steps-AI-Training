from weaviate.classes.query import MetadataQuery, Filter
from color_mapping import closest_color_name
import weaviate

gender_map = {"MALE": "nam", "FEMALE": "nữ", "UNISEX": "cả nam và nữ"}


def get_description(name, price, brand, sizes, features):
    category = features.get('category', 'khác').lower()
    gender = gender_map.get(features.get('gender', 'UNISEX'), 'cả nam và nữ')
    upper_material = features.get('upperMaterial', 'khác').lower().replace('+', 'và')
    sole_material = features.get('soleMaterial', 'khác').lower().replace('+', 'và')
    breathability = features.get('breathability', '').lower()
    durability_rating = features.get('durabilityRating', 1)
    occasion_tags = ', '.join(map(str.lower, features.get('occasionTags', [])))
    design_tags = ', '.join(map(str.lower, features.get('designTags', [])))
    primary_color = features.get('primaryColor') or ""
    secondary_color = features.get('secondaryColor') or ""
    color = (
        f"{closest_color_name(primary_color)}"
        if secondary_color == ""
        else f"{closest_color_name(primary_color)}, kết hợp với {closest_color_name(secondary_color)}"
    )
    durability = (
        'trung bình' if durability_rating <= 5.0 else 'khá' if durability_rating <= 8.0 else 'cao'
    )

    parts = [
        f"{name} của {brand}",
        f"giá {price} VND",
        f"thuộc loại {category}" if category else "",
        f"phù hợp cho {gender}" if gender else "",
        f"chất liệu thân {upper_material}" if upper_material else "",
        f"đế {sole_material}" if sole_material else "",
        f"màu chủ đạo {color}" if color else "",
        f"độ bền {durability}" if durability else "",
        f"thoáng khí {breathability}" if breathability else "",
        f"phong cách thiết kế: {design_tags}" if design_tags else "",
        f"phù hợp dịp: {occasion_tags}" if occasion_tags else "",
        f"kích thước: {', '.join(sizes)}" if sizes else "",
    ]

    description = ". ".join([p for p in parts if p]) + "."
    return description


def store_description(product_id, name, price, brand, sizes, features):
    client = weaviate.connect_to_local()

    if client.is_ready():
        collection = client.collections.get(name="ProductDescription")

        data = {
            "description": get_description(name, price, brand, sizes, features),
            "productId": product_id,
        }

        collection.data.insert(data)
        print(f"✅ Store description vector successfully for product ID: {product_id}")
        client.close()
    else:
        print("❌ Connection failed")
        client.close()


def semantic_search(query):
    client = weaviate.connect_to_local()

    if client.is_ready():
        collection = client.collections.get(name="ProductDescription")

        search_result = collection.query.near_text(
            query=query,
            return_properties=["productId"],
            return_metadata=MetadataQuery(certainty=True),
            limit=8,
        )

        groups = {}
        for item in search_result.objects:
            pid = item.properties["productId"]
            certainty = item.metadata.certainty
            if pid not in groups or certainty > groups[pid]:
                groups[pid] = certainty

        detections = sorted(groups.items(), key=lambda x: x[1], reverse=True)[:6]

        client.close()
        return detections
    else:
        print("❌ Connection failed")
        client.close()


def delete_description(product_id):
    client = weaviate.connect_to_local()

    if client.is_ready():
        collection = client.collections.get(name="ProductDescription")

        collection.data.delete_many(where=Filter.by_property("productId").equal(product_id))
        print(f"✅ Deleted description for product ID: {product_id}")

        client.close()
    else:
        print("❌ Connection failed")
        client.close()
