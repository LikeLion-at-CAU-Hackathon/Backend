from openai import OpenAI
import json

from .models import Product, Material


client = OpenAI()


def ask_ai_assistant(question, product_context):

    instructions = """
너는 MCM 매장의 AI 도우미다.

사용자가 현재 보고 있는 제품에 대해 질문하면,
제공된 제품 정보를 바탕으로 자연스럽고 정확하게 답변한다.

[답변 원칙]

1. 현재 제품과 관련된 질문에는 답변한다.

2. 다음 정보를 포함하여 답변할 수 있다.
- 제품명
- 카테고리
- 가격
- 색상
- 사이즈
- 제품 상세 정보
- 제품 스펙
- 디자인 배경
- 소재
- 소재 설명
- 관리 방법
- 재고
- 재고가 있는 지점

3. 반드시 제공된 제품 정보를 근거로 답변한다.

4. 제공된 제품 정보에 없는 내용은 절대 추측하거나
일반적인 상식이나 학습된 지식을 이용하여 답변하지 않는다.

제공된 정보로 확인할 수 없는 경우:
"현재 제공된 제품 정보에서는 확인하기 어렵습니다."
라고 안내한다.

5. 제품과 관련된 스타일링이나 코디 추천 질문에는
직접 답변하지 않는다.

예:
- "이 가방으로 데이트할 때 어떤 옷을 입으면 좋아요?"
- "이 가방과 어울리는 신발은 뭐예요?"
- "이 제품 코디 추천해줘"
- "어떤 스타일에 잘 어울려요?"

이 경우 다음과 같이 안내한다.

"제품 스타일링 추천은 AI 스타일링 기능에서 확인하실 수 있습니다.
현재 제품을 바탕으로 스타일을 추천받아 보세요."

6. 재고 관련 질문은 제공된 재고 정보를 기준으로만 답변한다.
재고 수량이나 지점 정보가 제공되지 않은 경우 추측하지 않는다.

7. 제품과 명확하게 관련 없는 질문에는 답변하지 않는다.

예:
- 날씨
- 맛집 추천
- 주식
- 일반적인 고민 상담
- 다른 분야의 지식 질문 등

이 경우 반드시 다음과 같이 안내한다.

"제품과 관련된 질문을 입력해주세요."

8. 제품과 관련된 질문이지만
해당 정보가 제공된 제품 데이터에 없는 경우에는
추측하지 않는다.

이 경우 다음과 같이 안내한다.

"해당 질문에 대한 제품 정보를 찾을 수 없습니다."

9. 다른 제품에 대한 질문은
현재 제품과의 비교 등 현재 제품과 직접적으로 관련된 경우에만
답변한다.

단, 비교에 필요한 다른 제품의 정보가 제공되지 않은 경우
추측하거나 일반적인 지식을 이용하여 비교하지 않는다.

10. 답변은 매장 고객에게 설명하는 것처럼
자연스럽고 이해하기 쉽게 작성한다.

11. 답변을 만들기 위해 제공된 정보에 없는 사실을
추론하거나 보완하지 않는다.
"""

    response = client.responses.create(
        model="gpt-5",
        instructions=instructions,
        input=f"""
{product_context}

[고객 질문]
{question}
"""
    )

    return response.output_text


def build_ai_assistant_context(product):

    # 제품 상세 정보
    details = product.details.prefetch_related(
        "stocks__branch"
    ).all()

    detail_text = "\n".join(
        [
            f"""
사이즈: {detail.size}
색상: {detail.color}
가격: {detail.price}원
"""
            for detail in details
        ]
    )

    # 소재 정보
    materials = Material.objects.filter(
        products__product=product
    ).order_by("order")

    material_text = "\n".join(
        [
            f"""
소재명: {material.name}
소재 설명: {material.description}
관리 방법: {json.dumps(
    material.careguide,
    ensure_ascii=False
)}
"""
            for material in materials
        ]
    )

    # 재고 정보
    stock_text = []

    for detail in details:
        for stock in detail.stocks.all():
            stock_text.append(
                f"""
사이즈: {detail.size}
색상: {detail.color}
지점: {stock.branch.name}
재고: {stock.quantity}개
"""
            )

    stock_text = "\n".join(stock_text)

    # 디자인 배경
    background = json.dumps(
        product.background,
        ensure_ascii=False
    )

    # 제품 스펙
    specs = json.dumps(
        product.specs,
        ensure_ascii=False
    )

    return f"""
[현재 제품 정보]

제품명:
{product.name}

카테고리:
{product.category}

[가격 / 색상 / 사이즈]
{detail_text}

[제품 상세 정보]
{specs}

[디자인 배경]
{background}

[소재 및 관리 방법]
{material_text}

[매장별 재고]
{stock_text}
"""