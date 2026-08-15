import json

from openai import OpenAI


client = OpenAI()

from django.db import transaction

from products.models import Product
from .models import (
    VisitHistory,
    SavedProduct,
    StyleProfile,
    StyleChip,
    Look,
    LookProduct,
)


# 규칙 (StyleChip 판단 규칙)
STYLE_RULES = {
    "WARM": {
        "cognac": 5,
        "brown": 4,
        "beige": 4,
        "camel": 4,
        "tan": 3,
        "gold": 2,
        "warm": 3,
    },

    "COMPACT": {
        "mini": 5,
        "small": 4,
        "compact": 5,
        "petite": 4,
        "micro": 4,
    },

    "CLASSIC": {
        "classic": 5,
        "structured": 4,
        "timeless": 4,
        "elegant": 3,
        "formal": 3,
        "traditional": 3,
    },

    "HERITAGE": {
        "heritage": 5,
        "visetos": 5,
        "monogram": 5,
        "signature": 4,
        "iconic": 3,
        "traditional": 3,
    },

    "REFINED": {
        "refined": 5,
        "polished": 4,
        "sophisticated": 4,
        "clean": 3,
        "elegant": 3,
        "understated": 3,
    },

    "MODERN": {
        "modern": 5,
        "contemporary": 5,
        "minimal": 4,
        "sleek": 4,
        "geometric": 3,
        "clean": 2,
    },

    "SOFT": {
        "soft": 5,
        "feminine": 4,
        "pastel": 4,
        "curved": 3,
        "delicate": 3,
        "light": 2,
    },

    "CASUAL": {
        "casual": 5,
        "relaxed": 4,
        "everyday": 4,
        "comfortable": 3,
        "denim": 3,
        "weekend": 3,
    },
}


# 분석 대상 제품 선택
def get_analysis_products(visit_session):
    """
    비로그인:
    - 현재 방문에서 최근 본 서로 다른 제품 최대 5개

    로그인:
    - 저장 제품 우선
    - 부족하면 현재 방문의 최근 본 제품으로 채움
    - 서로 다른 제품 총 최대 7개
    """

    products = []
    seen_ids = set()

    # ======================================
    # 비로그인
    # ======================================
    if visit_session.user is None:
        histories = (
            VisitHistory.objects
            .filter(visit_session=visit_session)
            .select_related("product")
            .order_by("-visited_at")
        )

        for history in histories:
            if history.product_id in seen_ids:
                continue

            products.append(history.product)
            seen_ids.add(history.product_id)

            if len(products) == 5:
                break

        return products

    # ======================================
    # 로그인
    # ======================================

    # 1. SavedProduct 우선
    saved_products = (
        SavedProduct.objects
        .filter(user=visit_session.user)
        .select_related("product")
        .order_by("-created_at")
    )

    for saved in saved_products:
        if saved.product_id in seen_ids:
            continue

        products.append(saved.product)
        seen_ids.add(saved.product_id)

        if len(products) == 7:
            return products

    # 2. 부족하면 VisitHistory
    histories = (
        VisitHistory.objects
        .filter(visit_session=visit_session)
        .select_related("product")
        .order_by("-visited_at")
    )

    for history in histories:
        if history.product_id in seen_ids:
            continue

        products.append(history.product)
        seen_ids.add(history.product_id)

        if len(products) == 7:
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

# 상위 3개의 StyleChip 선택
def select_style_chips(products):
    scores = calculate_style_scores(products)

    ranked_styles = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    positive_styles = [
        (code, score)
        for code, score in ranked_styles
        if score > 0
    ]

    if len(positive_styles) < 3:
        raise ValueError(
            "StyleProfile을 생성하기에 충분한 스타일 특징이 없습니다."
        )

    top_codes = [
        code
        for code, score in positive_styles[:3]
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
    # 1. 규칙 기반 StyleProfile 생성
    profile_result = create_style_profile(
        visit_session
    )

    style_profile = profile_result["profile"]

    # 2. Mock Look 3개 생성
    looks = create_mock_looks(
        style_profile
    )

    return {
        "profile": style_profile,
        "products": profile_result["products"],
        "style_chips": profile_result["style_chips"],
        "scores": profile_result["scores"],
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
def save_looks(style_profile, look_data_list):
    if len(look_data_list) != 3:
        raise ValueError("Look은 정확히 3개여야 합니다.")

    style_profile.looks.all().delete()

    created_looks = []

    for look_data in look_data_list:
        chip_codes = look_data["style_chips"]

        chips = list(
            StyleChip.objects.filter(code__in=chip_codes)
        )

        if len(chips) != len(chip_codes):
            raise ValueError(
                f"존재하지 않는 StyleChip이 있습니다: {chip_codes}"
            )

        look = Look.objects.create(
            style_profile=style_profile,
            look_order=look_data["look_order"],
            title=look_data["title"],
            subtitle=look_data.get("subtitle", ""),
            description=look_data["description"],
            reason=look_data["reason"],
        )

        look.style_chips.set(chips)

        items = look_data["items"]

        required_types = {
            "BAG",
            "TOP",
            "BOTTOM",
            "SHOES",
            "ACCESSORY",
        }

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
                "각 Look은 BAG, TOP, BOTTOM, SHOES, ACCESSORY를 하나씩 포함해야 합니다."
            )

        for item_data in items:
            product = Product.objects.filter(
                id=item_data["product_id"]
            ).first()

            if product is None:
                raise ValueError(
                    f"존재하지 않는 Product ID입니다: {item_data['product_id']}"
                )

            LookProduct.objects.create(
                look=look,
                product=product,
                item_type=item_data["item_type"],
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
        look_data_list
    )

    return looks