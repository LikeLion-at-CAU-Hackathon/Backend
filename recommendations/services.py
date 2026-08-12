def build_product_context(products):
    result = []

    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "color": product.color,
            "size": product.size,
            "collection": (
                product.collection.name
                if product.collection
                else None
            ),
            "specs": [
                {
                    "label": spec.label,
                    "value": spec.value
                }
                for spec in product.specs.all()
            ]
        })

    return result