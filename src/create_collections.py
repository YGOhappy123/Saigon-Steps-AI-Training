import weaviate
from weaviate.classes.config import Configure, Property, DataType


def recreate_collections():
    client = weaviate.connect_to_local()

    if client.is_ready():
        client.collections.delete_all()

        client.collections.create(
            name="ProductImage",
            description="Product image embeddings for image-based search",
            vector_config=Configure.Vectors.img2vec_neural(
                name="image_vector", image_fields=["image"]
            ),
            properties=[
                Property(name="image", data_type=DataType.BLOB),
                Property(name="productId", data_type=DataType.INT),
            ],
        )
        client.collections.create(
            name="ProductDescription",
            description="Text descriptions for semantic search",
            vector_config=Configure.Vectors.text2vec_transformers(
                name="description_vector", source_properties=["description"]
            ),
            properties=[
                Property(name="description", data_type=DataType.TEXT),
                Property(name="productId", data_type=DataType.INT),
            ],
        )

        print("✅ Create collections successfully")
        client.close()
    else:
        print("❌ Connection failed")
        client.close()


if __name__ == "__main__":
    recreate_collections()
