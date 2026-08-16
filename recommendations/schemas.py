# Response Schema
LOOK_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "looks": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "look_order": {
                        "type": "integer",
                        "enum": [1, 2, 3],
                    },
                    "style_chip": {
                        "type": "string",
                        "enum": [
                            "CLASSIC",
                            "HERITAGE",
                            "REFINED",
                            "CONTEMPORARY",
                            "MINIMAL",
                            "FEMININE",
                            "BOLD",
                            "CASUAL",
                            "PLAYFUL",
                        ],
                    },
                    "title": {
                        "type": "string",
                    },
                    "subtitle": {
                        "type": "string",
                    },
                    "description": {
                        "type": "string",
                    },
                    "reason": {
                        "type": "string",
                    },
                    "items": {
                        "type": "array",
                        "minItems": 5,
                        "maxItems": 5,
                        "items": {
                            "type": "object",
                            "properties": {
                                "item_type": {
                                    "type": "string",
                                    "enum": [
                                        "BAG",
                                        "TOP",
                                        "BOTTOM",
                                        "SHOES",
                                        "ACCESSORY",
                                    ],
                                },
                                "product_id": {
                                    "type": "integer",
                                },
                                "source": {
                                    "type": "string",
                                    "enum": [
                                        "VISITED",
                                        "RECOMMENDED",
                                    ],
                                },
                            },
                            "required": [
                                "item_type",
                                "product_id",
                                "source",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": [
                    "look_order",
                    "style_chip",
                    "title",
                    "subtitle",
                    "description",
                    "reason",
                    "items",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "looks",
    ],
    "additionalProperties": False,
}