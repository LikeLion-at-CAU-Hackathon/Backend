import json

from openai import OpenAI


client = OpenAI()

# 제폼 정보를 AI 가 읽기 쉬운 dict 형식으로 변환
def build_product_context(products):
    product_context = []

    for product in products:
        product_context.append({
            "id": product.id,
            "name": product.name,
            "color": product.color,
            "size": product.size,
            "collection": (
                product.collection.name
                if product.collection
                else None
            ),
            "specs": product.specs,
        })

    return product_context


# StyleProfile 생성하는 함수
def generate_style_profile(product_context, analysis_mode):

    prompt = f"""
You are an AI style assistant for an MCM retail experience.

Analyze only the products explored or saved during the customer's current visit.

Analysis mode:
{analysis_mode}

Products:
{json.dumps(product_context, ensure_ascii=False)}

Rules:
- Do not claim permanent preferences.
- Describe only current interests observed during this visit.
- Generate 2 to 4 concise style-interest tags.
- Use phrases such as "Warm Tone Interest", "Compact Bag Interest", or "Classic Styling".
- If analysis_mode is SINGLE_PRODUCT, avoid claiming behavioral patterns.
- For SINGLE_PRODUCT, phrase the summary as being based on the currently explored product.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "style_profile",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string"
                        },
                        "tags": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": [
                        "summary",
                        "tags"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.output_text)