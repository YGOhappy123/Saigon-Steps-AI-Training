from weaviate.classes.query import MetadataQuery, Filter
import weaviate


def get_similar_products(product_id):
    client = weaviate.connect_to_local()

    if client.is_ready():
        collection = client.collections.get(name="ProductDescription")

        response = collection.query.fetch_objects(
            filters=Filter.by_property("productId").equal(int(product_id)), limit=1
        )

        if not response.objects:
            client.close()
            return []
        else:
            queryProduct = response.objects[0]

            limit = 8
            search_result = collection.query.near_object(
                near_object=queryProduct.uuid,
                return_properties=["productId"],
                return_metadata=MetadataQuery(certainty=True),
                limit=limit + 1,
            )

            groups = {}
            for item in search_result.objects:
                pid = item.properties["productId"]
                if pid == product_id:
                    continue

                certainty = item.metadata.certainty
                if pid not in groups or certainty > groups[pid]:
                    groups[pid] = certainty

            detections = sorted(groups.items(), key=lambda x: x[1], reverse=True)[:limit]

            client.close()
            return detections
    else:
        print("❌ Connection failed")
        client.close()
