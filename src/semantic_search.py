from weaviate.classes.query import MetadataQuery, Filter
from color_mapping import closest_color_name
import weaviate

gender_map = {"MALE": "nam", "FEMALE": "nữ", "UNISEX": "cả nam và nữ"}


def get_description(name, price, brand, sizes, features):
    release_year = features.get('releaseYear', 2025)
    category = features.get('category', 'khác').lower()
    gender = gender_map.get(features.get('gender', 'UNISEX'), 'cả nam và nữ')
    upper_material = features.get('upperMaterial', 'khác').lower().replace('+', 'và')
    sole_material = features.get('soleMaterial', 'khác').lower().replace('+', 'và')
    lining_material = features.get('liningMaterial', 'khác').lower().replace('+', 'và')
    closure_type = features.get('closureType', 'khác').lower()
    pattern = features.get('pattern', 'khác').lower()
    water_resistant = features.get('waterResistant', '').lower()
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

    return (
        f"{name} là một sản phẩm đến từ thương hiệu {brand}, "
        + f"phát hành năm {release_year} và hiện đang được bán với giá {price} VND. "
        + f"Sản phẩm có các kích thước: {', '.join(sizes)}. "
        + f"Sản phẩm thuộc phân loại {category}, phù hợp cho {gender}. "
        + f"Phần thân của sản phẩm được làm từ chất liệu {upper_material}, "
        + f"kết hợp với phần đế {sole_material} cùng phần lót {lining_material}. "
        + f"Sản phẩm sử dụng kiểu đóng/ mở {closure_type} và có họa tiết {pattern}. "
        + f"Sản phẩm có khả năng chống nước {water_resistant}, độ bền {durability} và độ thoáng khí {breathability}, "
        + f"phù hợp cho các dịp như: {occasion_tags}. "
        + f"Sản phẩm mang màu sắc chủ đạo là {color}, "
        + f"nổi bật nên phong cách thiết kế mang phong cách: {design_tags}."
    )


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
            limit=5,
        )

        groups = {}
        for item in search_result.objects:
            pid = item.properties["productId"]
            certainty = item.metadata.certainty
            if pid not in groups or certainty > groups[pid]:
                groups[pid] = certainty

        detections = sorted(groups.items(), key=lambda x: x[1], reverse=True)[:5]

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
