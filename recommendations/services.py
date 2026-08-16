import json

from openai import OpenAI


client = OpenAI()

from django.db import transaction

from products.models import Product
from .models import (
    VisitHistory,
    StyleProfile,
    StyleChip,
    Look,
    LookProduct,
)


# 규칙 (StyleChip 판단 규칙)
STYLE_RULES = {
    "CLASSIC": {
        "classic": 5,
        "timeless": 4,
        "structured": 4,
        "elegant": 3,
        "traditional": 3,
    },

    "HERITAGE": {
        "heritage": 5,
        "monogram": 5,
        "signature": 4,
        "iconic": 4,
        "traditional": 3,
    },

    "REFINED": {
        "refined": 5,
        "polished": 4,
        "sophisticated": 4,
        "elegant": 3,
        "clean": 2,
    },

    "CONTEMPORARY": {
        "contemporary": 5,
        "modern": 4,
        "sleek": 4,
        "geometric": 3,
        "urban": 3,
    },

    "MINIMAL": {
        "minimal": 5,
        "simple": 4,
        "clean": 4,
        "understated": 4,
        "sleek": 3,
    },

    "FEMININE": {
        "feminine": 5,
        "soft": 4,
        "delicate": 4,
        "pastel": 3,
        "curved": 3,
    },

    "BOLD": {
        "bold": 5,
        "statement": 5,
        "contrast": 4,
        "graphic": 4,
        "vibrant": 3,
    },

    "CASUAL": {
        "casual": 5,
        "relaxed": 4,
        "everyday": 4,
        "comfortable": 3,
        "weekend": 3,
    },

    "PLAYFUL": {
        "playful": 5,
        "colorful": 4,
        "fun": 4,
        "quirky": 4,
        "bright": 3,
    },
}

# 분석 대상 제품 선택
def get_analysis_products(visit_session):
    """
    현재 방문 세션의 최근 NFC 제품 중
    서로 다른 제품 최대 3개를 반환한다.
    """

    histories = (
        VisitHistory.objects
        .filter(visit_session=visit_session)
        .select_related("product")
        .order_by("-visited_at")
    )

    products = []
    seen_ids = set()

    for history in histories:
        if history.product_id in seen_ids:
            continue

        products.append(history.product)
        seen_ids.add(history.product_id)

        if len(products) == 3:
            break

    return products


# 제품 특징 추출
def extract_product_features(product):
    """
    Product와 관련된 스타일 분석용 문자열을 만든다.
    """

    features = []

    # 기본 Product 정보
    features.append(product.name)
    features.append(product.category)

    # specs
    if product.specs:
        if isinstance(product.specs, list):
            for spec in product.specs:
                features.append(str(spec))

        elif isinstance(product.specs, dict):
            for key, value in product.specs.items():
                features.append(str(key))
                features.append(str(value))

    # background
    if product.background:
        if isinstance(product.background, dict):
            for key, value in product.background.items():
                features.append(str(key))
                features.append(str(value))

        elif isinstance(product.background, list):
            for value in product.background:
                features.append(str(value))

        else:
            features.append(str(product.background))

    # ProductDetail
    for detail in product.details.all():
        features.append(detail.color)
        features.append(detail.size)

    # Material
    for material_product in product.materials.select_related("material"):
        material = material_product.material

        features.append(material.name)
        features.append(material.description)

    return " ".join(
        feature.lower()
        for feature in features
        if feature
    )


# StyleChip 별 점수 계산
def calculate_style_scores(products):
    scores = {
        style_code: 0
        for style_code in STYLE_RULES
    }

    for product in products:
        product_text = extract_product_features(product)

        for style_code, rules in STYLE_RULES.items():

            for keyword, weight in rules.items():

                if keyword.lower() in product_text:
                    scores[style_code] += weight

    return scores

# 제품 하나에 대한 StyleChip 점수 계산
def get_product_style_scores(product):
    return calculate_style_scores([product])

# 상위 3개의 StyleChip 선택
def select_style_chips(products):
    scores = calculate_style_scores(products)

    ranked_styles = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_codes = [
        code
        for code, score in ranked_styles[:3]
    ]

    chips = StyleChip.objects.filter(
        code__in=top_codes
    )

    chip_map = {
        chip.code: chip
        for chip in chips
    }

    selected_chips = [
        chip_map[code]
        for code in top_codes
    ]

    if len(selected_chips) != 3:
        raise ValueError(
            "StyleChip 데이터를 확인해주세요."
        )

    return selected_chips, scores


# summary 생성 (AI 사용X)
def create_summary(style_chips):
    labels = [
        chip.label
        for chip in style_chips
    ]

    return (
        f"이번 탐색에서는 "
        f"{labels[0]}, {labels[1]}, {labels[2]} "
        f"스타일에 대한 관심이 나타났어요."
    )


# 전체 분석 함수
def analyze_visit_session(visit_session):

    # 1. 최근 NFC 제품 최대 3개
    visited_products = get_analysis_products(
        visit_session
    )

    if not visited_products:
        raise ValueError(
            "분석할 방문 제품이 없습니다."
        )

    # 2. 규칙 기반 StyleProfile 생성
    profile_result = create_style_profile(
        visit_session
    )

    style_profile = profile_result["profile"]

    # 3. StyleChip 3개 가져오기
    style_chips = list(
        style_profile.style_chips.all()
    )

    # 4. 방문 제품을 각 StyleChip / Look에 배치
    assignments = assign_products_to_style_chips(
        visited_products,
        style_chips
    )

     # 5. AI Look 생성 + 저장
    looks = create_ai_looks(
        style_profile,
        assignments,
        visited_products
    )

    return {
        "profile": style_profile,
        "products": visited_products,
        "looks": looks,
    }


# Style Profile 생성 함수
def create_style_profile(visit_session):
    # 1. 분석 대상 제품 선정
    products = get_analysis_products(
        visit_session
    )

    if not products:
        raise ValueError(
            "분석할 제품이 없습니다."
        )

    # 2. 규칙 기반 StyleChip 3개 선택
    style_chips, scores = select_style_chips(
        products
    )

    # 3. summary
    summary = create_summary(
        style_chips
    )

    # 4. DB 저장
    with transaction.atomic():

        profile, _ = StyleProfile.objects.update_or_create(
            visit_session=visit_session,
            defaults={
                "summary": summary
            }
        )

        profile.style_chips.set(
            style_chips
        )

    return {
        "profile": profile,
        "products": products,
        "style_chips": style_chips,
        "scores": scores,
    }




# mock 으로 looks 테스트
def generate_mock_looks(style_profile):
    return [
        {
            "look_order": 1,
            "title": "Heritage Weekend",
            "subtitle": "Classic & Heritage",
            "description": "클래식한 헤리티지 무드의 스타일링입니다.",
            "reason": "최근 탐색에서 나타난 클래식하고 헤리티지한 특성을 바탕으로 구성했어요.",
            "style_chips": ["CLASSIC", "HERITAGE"],
            "items": [
                {"item_type": "BAG", "product_id": 1},
                {"item_type": "TOP", "product_id": 2},
                {"item_type": "SHOES", "product_id": 4},
                {"item_type": "ACCESSORY", "product_id": 5},
                {"item_type": "BOTTOM", "product_id": 3},
            ],
        },
        {
            "look_order": 2,
            "title": "Refined City",
            "subtitle": "Refined & Modern",
            "description": "정돈된 무드에 현대적인 감각을 더한 스타일링입니다.",
            "reason": "최근 탐색에서 나타난 정제된 취향을 현대적으로 확장했어요.",
            "style_chips": ["REFINED", "MODERN"],
            "items": [
                {"item_type": "BAG", "product_id": 1},
                {"item_type": "TOP", "product_id": 2},
                {"item_type": "BOTTOM", "product_id": 3},
                {"item_type": "SHOES", "product_id": 4},
                {"item_type": "ACCESSORY", "product_id": 5},
            ],
        },
        {
            "look_order": 3,
            "title": "Soft Heritage",
            "subtitle": "Heritage & Soft",
            "description": "헤리티지 요소에 부드러운 분위기를 더한 스타일링입니다.",
            "reason": "헤리티지한 취향을 유지하면서 부드러운 분위기를 더했어요.",
            "style_chips": ["HERITAGE", "SOFT"],
            "items": [
                {"item_type": "BAG", "product_id": 1},
                {"item_type": "TOP", "product_id": 2},
                {"item_type": "BOTTOM", "product_id": 3},
                {"item_type": "SHOES", "product_id": 4},
                {"item_type": "ACCESSORY", "product_id": 5},
            ],
        },
    ]


# looks 저장
@transaction.atomic
def save_looks(
    style_profile,
    look_data_list,
    visited_products
):
    # =====================================
    # 0. 기본 검증
    # =====================================

    if len(look_data_list) != 3:
        raise ValueError(
            "Look은 정확히 3개여야 합니다."
        )

    if not visited_products:
        raise ValueError(
            "방문 제품이 최소 1개 이상 필요합니다."
        )

    # 실제 분석에 사용된 방문 제품 ID
    visited_product_ids = {
        product.id
        for product in visited_products
    }

    # StyleProfile에 실제 연결된 StyleChip
    profile_chip_codes = set(
        style_profile.style_chips.values_list(
            "code",
            flat=True
        )
    )

    if len(profile_chip_codes) != 3:
        raise ValueError(
            "StyleProfile에는 정확히 3개의 StyleChip이 있어야 합니다."
        )

    required_types = {
        LookProduct.ItemType.BAG,
        LookProduct.ItemType.TOP,
        LookProduct.ItemType.BOTTOM,
        LookProduct.ItemType.SHOES,
        LookProduct.ItemType.ACCESSORY,
    }

    valid_sources = {
        LookProduct.Source.VISITED,
        LookProduct.Source.RECOMMENDED,
    }

    # 전체 Look에서 사용된 StyleChip
    used_chip_codes = set()

    # 전체 Look에서 실제 VISITED로 사용된 상품
    used_visited_product_ids = set()

    # =====================================
    # 1. 먼저 전체 입력 데이터 검증
    # =====================================
    #
    # DB에 Look을 생성하기 전에 검증을 최대한 끝낸다.
    # =====================================

    look_orders = set()

    for look_data in look_data_list:
        # -----------------------------
        # Look order 검증
        # -----------------------------

        look_order = look_data["look_order"]

        if look_order in look_orders:
            raise ValueError(
                f"look_order가 중복되었습니다: {look_order}"
            )

        look_orders.add(look_order)

        # -----------------------------
        # StyleChip 검증
        # -----------------------------

        chip_code = look_data["style_chip"]

        if chip_code not in profile_chip_codes:
            raise ValueError(
                f"{chip_code}는 현재 StyleProfile의 "
                f"StyleChip이 아닙니다."
            )

        if chip_code in used_chip_codes:
            raise ValueError(
                f"{chip_code} StyleChip으로 "
                f"Look이 중복 생성되었습니다."
            )

        used_chip_codes.add(chip_code)

        # -----------------------------
        # items 검증
        # -----------------------------

        items = look_data["items"]

        if len(items) != 5:
            raise ValueError(
                "각 Look은 정확히 5개의 제품을 포함해야 합니다."
            )

        item_types = {
            item["item_type"]
            for item in items
        }

        if item_types != required_types:
            raise ValueError(
                "각 Look은 BAG, TOP, BOTTOM, SHOES, "
                "ACCESSORY를 하나씩 포함해야 합니다."
            )

        # 같은 Look에 같은 product 중복 방지
        product_ids = [
            item["product_id"]
            for item in items
        ]

        if len(product_ids) != len(set(product_ids)):
            raise ValueError(
                "같은 Look에 동일한 Product를 "
                "중복으로 포함할 수 없습니다."
            )

        # -----------------------------
        # source 검증
        # -----------------------------

        visited_count = 0

        for item in items:
            product_id = item["product_id"]
            source = item["source"]

            if source not in valid_sources:
                raise ValueError(
                    f"잘못된 source 값입니다: {source}"
                )

            # DB에 실제 존재하는 Product인지
            if not Product.objects.filter(
                id=product_id
            ).exists():
                raise ValueError(
                    f"존재하지 않는 Product ID입니다: "
                    f"{product_id}"
                )

            # VISITED라면 진짜 방문 상품이어야 함
            if source == LookProduct.Source.VISITED:
                if product_id not in visited_product_ids:
                    raise ValueError(
                        f"Product {product_id}는 "
                        f"실제 방문 제품이 아닙니다."
                    )

                visited_count += 1

                used_visited_product_ids.add(
                    product_id
                )

        # 각 Look에는 방문 상품 최소 1개
        if visited_count == 0:
            raise ValueError(
                "각 Look에는 방문 기록의 제품이 "
                "최소 1개 포함되어야 합니다."
            )

    # =====================================
    # 2. Look 전체 수준 검증
    # =====================================

    if used_chip_codes != profile_chip_codes:
        raise ValueError(
            "StyleProfile의 각 StyleChip마다 "
            "Look이 하나씩 생성되어야 합니다."
        )

    # 방문했던 모든 상품이 최소 하나의 Look에는 들어갔는지
    if used_visited_product_ids != visited_product_ids:
        missing_ids = (
            visited_product_ids
            - used_visited_product_ids
        )

        raise ValueError(
            "일부 방문 제품이 Look에 반영되지 않았습니다: "
            f"{sorted(missing_ids)}"
        )

    # =====================================
    # 3. 기존 Look 삭제
    # =====================================

    style_profile.looks.all().delete()

    # =====================================
    # 4. 실제 DB 저장
    # =====================================

    created_looks = []

    for look_data in look_data_list:
        chip_code = look_data["style_chip"]

        style_chip = StyleChip.objects.get(
            code=chip_code
        )

        look = Look.objects.create(
            style_profile=style_profile,
            style_chip=style_chip,
            look_order=look_data["look_order"],
            title=look_data["title"],
            subtitle=look_data.get(
                "subtitle",
                ""
            ),
            description=look_data["description"],
            reason=look_data["reason"],
        )

        for item_data in look_data["items"]:
            product = Product.objects.get(
                id=item_data["product_id"]
            )

            LookProduct.objects.create(
                look=look,
                product=product,
                item_type=item_data["item_type"],
                source=item_data["source"],
            )

        created_looks.append(look)

    return created_looks

# mock looks 생성
def create_mock_looks(style_profile):
    look_data_list = generate_mock_looks(
        style_profile
    )

    looks = save_looks(
        style_profile,
        look_data_list,
        visited_products=[]
    )

    return looks


# ======================================
# AI 기반 looks 생성

# 존재하는 Product 중에서만 LookProduct를 생성하도록 제한
def build_look_product_candidates():
    products = (
        Product.objects
        .prefetch_related(
            "details",
            "materials__material",
        )
        .all()
    )

    result = []

    for product in products:
        details = list(product.details.all())

        colors = list({
            detail.color
            for detail in details
            if detail.color
        })

        sizes = list({
            detail.size
            for detail in details
            if detail.size
        })

        materials = [
            link.material.name
            for link in product.materials.select_related("material")
        ]

        result.append({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "colors": colors,
            "sizes": sizes,
            "materials": materials,
            "specs": product.specs,
            "background": product.background,
        })

    return result

# AI 기반 Look 생성
def generate_ai_looks(
    style_profile,
    assignments
):
    profile_chips = list(
        style_profile.style_chips.values(
            "code",
            "label"
        )
    )

    product_candidates = build_look_product_candidates()

    # assignments 안에는 Product 객체가 들어 있으므로
    # AI에게 넘길 수 있도록 dict 형태로 변환
    required_products_by_chip = {}

    for chip_code, products in assignments.items():
        required_products_by_chip[chip_code] = [
            {
                "id": product.id,
                "name": product.name,
                "category": product.category,
            }
            for product in products
        ]

    prompt = f"""
You are an MCM fashion styling assistant.

Create exactly 3 curated looks.

The user's style profile contains exactly 3 style chips.

USER STYLE CHIPS:
{json.dumps(profile_chips, ensure_ascii=False)}

REQUIRED VISITED PRODUCTS FOR EACH STYLE CHIP:
{json.dumps(required_products_by_chip, ensure_ascii=False)}

AVAILABLE PRODUCTS:
{json.dumps(product_candidates, ensure_ascii=False)}

Rules:

1. Create exactly 3 looks.

2. Create exactly one Look for each USER STYLE CHIP.

3. Each Look must use exactly one style_chip.
   The style_chip must be one of USER STYLE CHIPS.

4. Each Look must contain exactly these five item types:
   BAG
   TOP
   BOTTOM
   SHOES
   ACCESSORY

5. Each item type must appear exactly once.

6. Every product listed in REQUIRED VISITED PRODUCTS
   for that style chip MUST be included in that Look.

7. Products from REQUIRED VISITED PRODUCTS must have:
   "source": "VISITED"

8. All other products must have:
   "source": "RECOMMENDED"

9. You MUST only use product IDs from AVAILABLE PRODUCTS.
   Never invent products or product IDs.

10. Never replace or omit a required visited product.

11. Two products of the same category cannot appear
    in the same Look.

12. Select recommended products that complement
    the required visited products based on:
    color,
    material,
    pattern,
    design,
    and overall style compatibility.

13. Each Look must contain exactly 5 products total.

14. Each Look should represent the styling direction
    of its assigned style_chip.

15. reason must explain:
    - how the visited product(s) influenced the styling
    - why the recommended products work with them
    - why the Look fits the assigned style chip

Return JSON only.

Required format:

{{
  "looks": [
    {{
      "look_order": 1,
      "style_chip": "CLASSIC",
      "title": "...",
      "subtitle": "...",
      "description": "...",
      "reason": "...",
      "items": [
        {{
          "item_type": "BAG",
          "product_id": 1,
          "source": "VISITED"
        }},
        {{
          "item_type": "TOP",
          "product_id": 2,
          "source": "RECOMMENDED"
        }},
        {{
          "item_type": "BOTTOM",
          "product_id": 3,
          "source": "RECOMMENDED"
        }},
        {{
          "item_type": "SHOES",
          "product_id": 4,
          "source": "RECOMMENDED"
        }},
        {{
          "item_type": "ACCESSORY",
          "product_id": 5,
          "source": "RECOMMENDED"
        }}
      ]
    }}
  ]
}}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    data = json.loads(
        response.output_text
    )

    return data["looks"]



def create_ai_looks(
    style_profile,
    assignments,
    visited_products
):
    look_data_list = generate_ai_looks(
        style_profile,
        assignments
    )

    looks = save_looks(
        style_profile,
        look_data_list,
        visited_products=visited_products
    )

    return looks


# Look 배치 함수 (최근 방문 제품을 3개의 Look에 배치)
def assign_visited_products_to_looks(products):
    """
    최근 방문 제품들을 3개의 Look에 배치한다.

    모든 Look에는 방문 제품이 최소 1개 포함되고,
    모든 방문 제품도 최소 하나의 Look에 포함된다.
    """

    if not products:
        raise ValueError("방문 기록이 없습니다.")

    # 제품 1개
    if len(products) == 1:
        product = products[0]

        return [
            [product],
            [product],
            [product],
        ]

    # 제품 2개
    if len(products) == 2:
        p1, p2 = products

        # 같은 category면 같은 Look에 넣지 않음
        if p1.category == p2.category:
            return [
                [p1],
                [p2],
                [p1],
            ]

        # 다른 category면 조합 가능
        return [
            [p1],
            [p2],
            [p1, p2],
        ]

    # 제품 3개
    p1, p2, p3 = products

    # 가장 단순하고 안전한 기본 배치
    return [
        [p1],
        [p2],
        [p3],
    ]


# 제품들을 StyleChip에 배치하는 함수
def assign_products_to_style_chips(products, style_chips):
    """
    방문 제품을 StyleChip별 Look에 배치한다.

    규칙:
    1. Look은 StyleChip 3개 각각 하나씩 존재
    2. 모든 Look에 방문 제품이 최소 1개 포함
    3. 제품이 1개면 세 Look에 모두 포함
    4. 같은 category의 제품은 같은 Look에 함께 들어갈 수 없음
    5. 제품은 자신과 가장 잘 맞는 StyleChip Look에 우선 배치
    """
    if not products:
        raise ValueError("분석할 방문 제품이 없습니다.")

    if len(style_chips) != 3:
        raise ValueError("StyleChip은 정확히 3개여야 합니다.")

    assignments = {
        chip.code: []
        for chip in style_chips
    }

    # 제품별 style 점수 미리 계산
    product_scores = {
        product.id: get_product_style_scores(product)
        for product in products
    }

    # ----------------------------
    # 제품 1개
    # ----------------------------
    if len(products) == 1:
        product = products[0]

        for chip in style_chips:
            assignments[chip.code].append(product)

        return assignments

    # ----------------------------
    # 제품 2개
    # ----------------------------
    if len(products) == 2:
        p1, p2 = products

        # 각 chip에서 어떤 제품이 더 잘 맞는지 계산
        for chip in style_chips:
            p1_score = product_scores[p1.id].get(
                chip.code,
                0
            )

            p2_score = product_scores[p2.id].get(
                chip.code,
                0
            )

            # 해당 chip과 더 잘 맞는 제품을 기본으로 배치
            if p1_score >= p2_score:
                assignments[chip.code].append(p1)
            else:
                assignments[chip.code].append(p2)

        # 두 제품 중 하나가 한 번도 사용되지 않았을 수도 있으므로 보정
        used_product_ids = {
            product.id
            for assigned_products in assignments.values()
            for product in assigned_products
        }

        for product in products:
            if product.id in used_product_ids:
                continue

            # 아직 사용되지 않은 제품이 가장 잘 맞는 chip 찾기
            best_chip = max(
                style_chips,
                key=lambda chip:
                    product_scores[product.id].get(
                        chip.code,
                        0
                    )
            )

            current_products = assignments[
                best_chip.code
            ]

            # 같은 카테고리라면 같이 넣을 수 없음
            category_exists = any(
                existing.category == product.category
                for existing in current_products
            )

            if not category_exists:
                assignments[
                    best_chip.code
                ].append(product)

            else:
                # 다른 chip 중 넣을 수 있는 곳 찾기
                for chip in style_chips:
                    current_products = assignments[
                        chip.code
                    ]

                    category_exists = any(
                        existing.category == product.category
                        for existing in current_products
                    )

                    if not category_exists:
                        assignments[
                            chip.code
                        ].append(product)
                        break

        return assignments

    # ----------------------------
    # 제품 3개
    # ----------------------------
    for product in products:
        ranked_chips = sorted(
            style_chips,
            key=lambda chip:
                product_scores[product.id].get(
                    chip.code,
                    0
                ),
            reverse=True
        )

        for chip in ranked_chips:
            current_products = assignments[
                chip.code
            ]

            category_exists = any(
                existing.category == product.category
                for existing in current_products
            )

            if category_exists:
                continue

            assignments[
                chip.code
            ].append(product)

            break

    # 비어 있는 Look 보정
    for chip in style_chips:
        if assignments[chip.code]:
            continue

        ranked_products = sorted(
            products,
            key=lambda product:
                product_scores[product.id].get(
                    chip.code,
                    0
                ),
            reverse=True
        )

        assignments[
            chip.code
        ].append(
            ranked_products[0]
        )

    return assignments

def remove_category_duplicates(products):
    result = []
    categories = set()

    for product in products:
        if product.category in categories:
            continue

        result.append(product)
        categories.add(product.category)

    return result