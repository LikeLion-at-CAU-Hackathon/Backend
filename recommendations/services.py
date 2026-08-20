from copy import deepcopy
import json
import base64

from openai import OpenAI

from django.db import transaction
from django.core.files.base import ContentFile

from products.models import Product, ProductImage
from .models import (   
    VisitHistory,
    StyleProfile,
    StyleChip,
    Look,
    LookProduct,
)
from .schemas import LOOK_RESPONSE_SCHEMA

from celery import group

client = OpenAI()


# 규칙 (StyleChip 판단 규칙)
STYLE_RULES = {

    # =====================================================
    # CLASSIC
    # 전통적이고 유행을 타지 않는 정돈된 스타일
    # =====================================================
    "CLASSIC": {
        "classic": 5,
        "클래식": 5,
        "timeless": 5,
        "타임리스": 5,

        "traditional": 4,
        "전통적": 4,

        "classic silhouette": 4,
        "클래식한 실루엣": 4,

        "structured": 3,
        "구조적인": 3,
        "구조감": 3,

        "v-neck": 2,
        "button closure": 2,
        "loafer": 3,
        "로퍼": 3,
        "cardigan": 2,
        "카디건": 2,
        "bouclé": 2,
        "부클레": 2,
    },


    # =====================================================
    # HERITAGE
    # MCM의 모노그램 / 상징 / 전통 / 브랜드 유산
    # =====================================================
    "HERITAGE": {
        "heritage": 5,
        "헤리티지": 5,

        "bavarian diamond": 5,
        "바이에른 다이아몬드": 5,
        "바이예른 다이아몬드": 5,

        "mcm luggage": 5,
        "mcm leather craftsmanship": 5,
        "mcm global nomad": 4,

        "iconic": 4,
        "아이코닉": 4,

        "signature": 4,
        "시그니처": 4,

        "laurel": 4,
        "라우렐": 4,

        "visetos": 3,
        "비세토스": 3,

        # 제품 대부분에 들어가므로 너무 높은 점수는 주지 않음
        "monogram": 2,
        "모노그램": 2,

        "emblem": 2,
        "엠블럼": 2,

        "house": 2,
        "하우스": 2,
    },


    # =====================================================
    # REFINED
    # 세련되고 정제된, 깔끔하게 완성된 스타일
    # =====================================================
    "REFINED": {
        "refined": 5,
        "정제된": 5,

        "polished": 5,
        "sophisticated": 5,
        "세련된": 5,

        "elegant": 4,
        "우아한": 4,

        "clean silhouette": 4,
        "깔끔한 실루엣": 4,

        "clean": 3,
        "깔끔한": 3,

        "structured silhouette": 3,
        "구조적인 실루엣": 3,

        "tailored": 3,
        "정교한": 3,

        "subtle": 3,
        "은은한": 2,

        "understated": 3,
        "절제된": 4,

        "smooth": 2,
        "부드러운 마감": 2,

        "고급스러운 마감": 3,
    },


    # =====================================================
    # MINIMAL
    # 장식을 절제하고 단순하며 깨끗한 스타일
    # =====================================================
    "MINIMAL": {
        "minimal": 5,
        "미니멀": 5,

        "simple": 5,
        "심플": 5,

        "understated": 5,
        "절제된": 5,

        "clean": 4,
        "깔끔한": 4,

        "clean silhouette": 4,
        "깔끔한 실루엣": 4,

        "sleek": 4,

        "tone-on-tone": 4,
        "tone on tone": 4,
        "톤온톤": 4,

        "monochrome": 4,
        "모노크롬": 4,

        "solid": 2,

        "subtle": 3,
        "은은한": 2,

        "simple silhouette": 4,
        "심플한 실루엣": 4,
    },


    # =====================================================
    # CONTEMPORARY
    # 전통적인 요소를 현대적으로 재해석한 스타일
    # =====================================================
    "CONTEMPORARY": {
        "contemporary": 5,
        "컨템포러리": 5,

        "modern": 5,
        "모던": 5,
        "현대적": 5,

        "modern reinterpretation": 5,
        "현대적으로 재해석": 5,
        "현대적인 재해석": 5,

        "geometric": 4,
        "geometric structure": 5,
        "기하학": 4,
        "기하학적인": 4,

        "linear": 3,
        "선형적인": 3,

        "structured": 3,
        "구조적인": 3,

        "platform": 2,
        "플랫폼": 2,

        "asymmetric": 3,
        "architectural": 4,

        "new silhouette": 3,
        "새로운 실루엣": 3,
    },


    # =====================================================
    # FEMININE
    # 부드러운 컬러 / 곡선 / 섬세한 실루엣
    # =====================================================
    "FEMININE": {
        "feminine": 5,
        "페미닌": 5,
        "여성스러운": 5,

        "soft pink": 3,
        "blush pink": 3,

        "pastel": 3,
        "파스텔": 3,

        "delicate": 4,
        "섬세한": 4,

        "curved": 4,
        "곡선": 4,
        "부드러운 곡선": 5,

        "drapey": 4,
        "drape": 4,
        "드레이프": 4,

        "cropped cardigan": 3,
        "크롭 카디건": 3,

        "cropped": 2,
        "크롭": 2,

        "v-neck": 2,

        "silk scarf": 3,
        "실크 스카프": 3,

        "ribbon": 2,
        "리본": 2,
    },


    # =====================================================
    # BOLD
    # 강한 그래픽 / 광택 / 대비 / 볼륨 / 스터드
    # =====================================================
    "BOLD": {
        "bold": 5,
        "볼드": 5,

        "statement": 5,
        "강한 존재감": 5,

        "graphic": 5,
        "그래픽": 5,

        "contrast": 4,
        "contrast detail": 4,
        "배색": 4,
        "대비": 4,

        "metallic": 4,
        "메탈릭": 4,

        "lurex": 5,
        "루렉스": 5,

        "sequin": 5,
        "시퀸": 5,

        "stud": 4,
        "studs": 4,
        "스터드": 4,

        "oversized": 4,
        "오버사이즈": 4,

        "maxi": 3,
        "맥시": 3,

        "platform": 3,
        "플랫폼": 3,

        "volume": 3,
        "볼륨": 3,

        "high-frequency print": 3,
    },


    # =====================================================
    # PLAYFUL
    # 재미 / 위트 / 컬러 / 시즌 그래픽 / 참 장식
    # =====================================================
    "PLAYFUL": {
        "playful": 5,
        "플레이풀": 5,

        "fun": 5,
        "위트": 5,

        "quirky": 5,

        "bear charm": 5,
        "베어 참": 5,

        "charm": 3,
        "참": 3,

        "disco": 5,
        "디스코": 5,

        "constellation": 5,
        "별자리": 5,

        "sequin": 4,
        "시퀸": 4,

        "colorful": 4,
        "컬러풀": 4,

        "bright": 3,

        "reversible": 3,
        "리버서블": 3,

        "ribbon": 3,
        "리본": 3,

        "graphic": 2,
        "그래픽": 2,
    },


    # =====================================================
    # CASUAL
    # 일상적이고 편안하며 부담 없이 착용 가능한 스타일
    # =====================================================
    "CASUAL": {
        "casual": 5,
        "캐주얼": 5,

        "everyday": 5,
        "데일리": 5,
        "일상": 4,
        "일상적인": 4,

        "relaxed": 4,
        "여유로운": 4,

        "comfortable": 4,
        "comfort": 4,
        "편안": 4,

        "regular fit": 3,

        "t-shirt": 3,
        "티셔츠": 3,

        "denim": 3,
        "데님": 3,

        "cotton jersey": 3,
        "코튼 저지": 3,

        "sneaker": 2,
        "sneakers": 2,
        "스니커즈": 2,

        "hands-free": 2,
        "핸즈프리": 2,
    },


    # =====================================================
    # URBAN
    # 도시적 / 기능적 / 구조적 / 모빌리티 중심
    # =====================================================
    "URBAN": {
        "urban": 5,
        "어반": 5,
        "도시적": 5,

        "mobility": 5,
        "모빌리티": 5,

        "hands-free": 4,
        "핸즈프리": 4,

        "crossbody": 4,
        "크로스바디": 4,

        "backpack": 4,
        "백팩": 4,

        "geometric": 4,
        "기하학": 4,

        "structured": 3,
        "구조적인": 3,

        "monochrome": 4,
        "모노크롬": 4,

        "oversized": 3,
        "오버사이즈": 3,

        "shopper": 2,
        "쇼퍼": 2,

        "low-top": 2,
        "로우탑": 2,

        "utility": 3,
        "functional": 3,
        "실용적인": 3,
        "실용성": 3,
    },


    # =====================================================
    # LUXURIOUS
    # 고급 소재 / 가죽 / 실크 / 캐시미어 / 골드 하드웨어
    # =====================================================
    "LUXURIOUS": {
        "luxurious": 5,
        "luxury": 5,
        "럭셔리": 5,

        "premium": 5,
        "고급스러운": 5,
        "고급": 4,

        "cashmere": 5,
        "캐시미어": 5,

        "silk": 5,
        "실크": 5,

        "24k gold": 5,
        "24k gold-plated": 5,
        "24k 골드": 5,

        "full-grain leather": 5,
        "풀그레인": 5,

        "italian calfskin": 5,
        "italian calf leather": 5,
        "이탈리아산 카프": 5,

        "lambskin": 4,
        "램스킨": 4,
        "양가죽": 4,

        "nappa leather": 4,
        "나파 가죽": 4,

        "calfskin": 3,
        "카프스킨": 3,

        "suede": 3,
        "스웨이드": 3,

        "superfine wool": 4,
        "슈퍼파인 울": 4,

        "gold-tone": 3,
        "골드톤": 3,
        "골드 톤": 3,

        # leather 자체는 너무 자주 등장하므로 낮게
        "leather": 1,
        "가죽": 1,
    },


    # =====================================================
    # SPORTY
    # 운동화 / 기능성 솔 / 쿠셔닝 / 메시 등의 스포츠 요소
    # =====================================================
    "SPORTY": {
        "sporty": 5,
        "스포티": 5,

        "sneaker": 5,
        "sneakers": 5,
        "스니커즈": 5,

        "running": 5,
        "러닝": 5,

        "low-top sneaker": 5,
        "low-top sneakers": 5,
        "로우탑 스니커즈": 5,

        "ortholite": 5,
        "ortholite®": 5,

        "memory foam": 4,
        "메모리 폼": 4,
        "메모리폼": 4,

        "rubber outsole": 4,
        "러버 아웃솔": 4,
        "고무 아웃솔": 4,

        "eva outsole": 4,
        "eva platform": 3,

        "vibram": 4,
        "vibram®": 4,

        "mesh": 4,
        "메시": 4,
        "메쉬": 4,

        "cushion": 3,
        "cushioning": 3,
        "쿠셔닝": 3,

        "footbed": 2,
        "풋베드": 2,

        "comfortable": 2,
        "편안한 착화감": 3,
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


def flatten_feature(value):
    """
    dict / list / 문자열을 재귀적으로 펼쳐서
    스타일 분석에 사용할 문자열 목록으로 변환한다.
    """

    features = []

    if value is None:
        return features

    if isinstance(value, dict):
        for key, val in value.items():
            features.append(str(key))
            features.extend(flatten_feature(val))

    elif isinstance(value, (list, tuple, set)):
        for item in value:
            features.extend(flatten_feature(item))

    else:
        features.append(str(value))

    return features


# 제품 특징 추출
def extract_product_features(product):
    """
    Product와 관련된 스타일 분석용 문자열을 만든다.
    """

    features = []

    # Product
    features.append(product.name)
    features.append(product.category)

    # specs
    features.extend(
        flatten_feature(product.specs)
    )

    # background
    features.extend(
        flatten_feature(product.background)
    )

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
        str(feature).lower()
        for feature in features
        if feature
    )

MAX_SCORE_PER_PRODUCT = 12

# StyleChip 별 점수 계산
def calculate_style_scores(products):
    scores = {
        style_code: 0
        for style_code in STYLE_RULES
    }

    for product in products:
        product_text = extract_product_features(product)

        for style_code, rules in STYLE_RULES.items():

            product_score = 0

            for keyword, weight in rules.items():

                if keyword.lower() in product_text:
                    product_score += weight

            # 한 제품이 특정 StyleChip에 지나치게
            # 많은 점수를 주는 것을 방지
            product_score = min(
                product_score,
                MAX_SCORE_PER_PRODUCT,
            )

            scores[style_code] += product_score

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
        f"현재 관심사를 분석한 결과, "
        f"{labels[0]}, {labels[1]}, {labels[2]} "
        f"스타일을 선호하고 있습니다."
    )


# 전체 분석 함수
def analyze_visit_session(visit_session):

    # 1. 최근 방문 제품 최대 3개
    visited_products = get_analysis_products(
        visit_session
    )

    if not visited_products:
        raise ValueError(
            "분석할 방문 제품이 없습니다."
        )

    # 2. StyleProfile 생성
    profile_result = create_style_profile(
        visit_session,
        visited_products
    )

    style_profile = profile_result["profile"]

    # 3. StyleChip 3개
    style_chips = profile_result["style_chips"]

    # 4. 가장 최근 제품은 모든 Look에 강제로 배치
    assignments = assign_products_to_style_chips(
        visited_products,
        style_chips
    )

    # 5. 2, 3번째 방문 제품은 optional
    optional_products = visited_products[1:]

    # 6. AI Look 생성
    look_data = generate_ai_looks(
        style_profile,
        assignments,
        optional_products
    )

    # 7. DB 저장
    looks = save_looks(
        style_profile,
        look_data,
        visited_products=visited_products
    )

    # 8. 이미지 생성 task 등록
    look_ids = [look.id for look in looks]

    def enqueue_image_tasks():
        from .tasks import generate_look_image_task

        group(
            generate_look_image_task.s(look_id)
            for look_id in look_ids
        ).apply_async()

    transaction.on_commit(
        enqueue_image_tasks
    )

    return {
        "status": "PROCESSING",
        "profile": style_profile,
        "products": visited_products,
        "looks": looks,
    }


# Style Profile 생성 함수
def create_style_profile(
    visit_session,
    products
):
    if not products:
        raise ValueError(
            "분석할 제품이 없습니다."
        )

    main_product = products[0]

    style_chips, scores = select_style_chips(
        products
    )

    summary = create_summary(
        style_chips
    )

    with transaction.atomic():
        profile = StyleProfile.objects.create(
            visit_session=visit_session,
            main_product=main_product,
            summary=summary,
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


def get_product_image(product):
    """
    Product에 연결된 대표 이미지 1장을 가져온다.
    """

    return (
        ProductImage.objects
        .filter(detail__product=product)
        .order_by("order", "id")
        .first()
    )

def generate_look_image(look):
    """
    Look에 포함된 5개 제품의 이미지를 OpenAI에 전달해서
    하나의 룩북 이미지를 생성하고 Look.image에 저장한다.
    """

    look_products = list(
        look.look_products
        .select_related("product")
        .all()
    )

    if len(look_products) != 5:
        raise ValueError(
            f"Look {look.id}에는 정확히 5개의 제품이 필요합니다."
        )

    image_files = []
    product_descriptions = []

    try:
        for index, look_product in enumerate(
            look_products,
            start=1,
        ):
            product = look_product.product

            product_image = get_product_image(product)

            if not product_image or not product_image.image:
                raise ValueError(
                    f"Product {product.id}의 이미지가 없습니다."
                )

            # OpenAI에 보낼 실제 이미지 파일
            image_files.append(
                open(product_image.image.path, "rb")
            )

            product_descriptions.append(
                f"{index}. "
                f"{product.category}: "
                f"{product.name}"
            )

        product_text = "\n".join(
            product_descriptions
        )

        prompt = f"""
Create a premium full-body fashion editorial image
using all five reference product images.

The reference images are provided in the same order
as the product list below.

PRODUCTS:
{product_text}

LOOK INFORMATION:
Title: {look.title}
Subtitle: {look.subtitle}
Description: {look.description}

Requirements:
- Use all five referenced products in one complete outfit.
- Include exactly one BAG, TOP, BOTTOM, SHOES, and ACCESSORY.
- Preserve each reference product as faithfully as possible.
- Preserve the original colors, shapes, patterns, materials,
  logos, and recognizable product details.
- Do not replace any referenced product with another design.
- Style the five products together naturally.
- Show a full-body fashion look.
- Premium luxury fashion editorial photography.
- Clean and sophisticated background.
- No text, captions, logos added to the background,
  or graphic overlays.
"""

        result = client.images.edit(
            model="gpt-image-2",
            image=image_files,
            prompt=prompt,
            # input_fidelity="high",
            size="1024x1536",
            quality="medium",
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(
            image_base64
        )

        filename = (
            f"look_"
            f"{look.style_profile_id}_"
            f"{look.look_order}.png"
        )

        look.image.save(
            filename,
            ContentFile(image_bytes),
            save=True,
        )

        return look.image

    finally:
        for image_file in image_files:
            image_file.close()

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

    # 최근 방문 제품 최대 3개
    visited_products = visited_products[:3]

    # 가장 최근 방문 제품
    main_product = visited_products[0]
    main_product_id = main_product.id

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

    required_types = set(Product.Category.values)

    valid_sources = {
        LookProduct.Source.VISITED,
        LookProduct.Source.RECOMMENDED,
    }

    used_chip_codes = set()
    look_orders = set()

    # =====================================
    # 1. 전체 입력 데이터 사전 검증
    # =====================================

    for look_data in look_data_list:

        # -----------------------------
        # look_order 검증
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

        # 같은 Look에 같은 Product 중복 방지
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
        # source + Product 검증
        # -----------------------------

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

            # VISITED라면 실제 최근 방문 제품이어야 함
            if source == LookProduct.Source.VISITED:
                if product_id not in visited_product_ids:
                    raise ValueError(
                        f"Product {product_id}는 "
                        f"실제 방문 제품이 아닙니다."
                    )

            # 실제 최근 방문 제품을 사용했다면
            # 반드시 VISITED로 표시되어야 함
            if product_id in visited_product_ids:
                if source != LookProduct.Source.VISITED:
                    raise ValueError(
                        f"방문 제품 {product_id}는 "
                        f"source가 VISITED여야 합니다."
                    )

        # -----------------------------
        # 핵심 규칙:
        # 가장 최근 방문 제품은 모든 Look에 반드시 포함
        # -----------------------------

        main_product_in_look = any(
            item["product_id"] == main_product_id
            and item["source"] == LookProduct.Source.VISITED
            for item in items
        )

        if not main_product_in_look:
            raise ValueError(
                "가장 최근 방문 제품은 "
                "모든 Look에 VISITED로 포함되어야 합니다."
            )

    # =====================================
    # 2. Look 전체 수준 검증
    # =====================================

    if used_chip_codes != profile_chip_codes:
        raise ValueError(
            "StyleProfile의 각 StyleChip마다 "
            "Look이 하나씩 생성되어야 합니다."
        )

    # look_order도 1, 2, 3 정확히 사용하도록 강제하고 싶다면
    if look_orders != {1, 2, 3}:
        raise ValueError(
            "look_order는 1, 2, 3을 정확히 하나씩 사용해야 합니다."
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
    assignments,
    optional_products
):
    profile_chips = list(
        style_profile.style_chips.values(
            "code",
            "label"
        )
    )
    profile_chip_codes = [
        chip["code"]
        for chip in profile_chips
    ]
    if len(profile_chip_codes) != 3:
        raise ValueError(
            "StyleProfile에는 정확히 3개의 StyleChip이 있어야 합니다."
        )

    product_candidates = build_look_product_candidates()

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

    optional_product_data = [
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
        }
        for product in optional_products
    ]

    # 현재 StyleProfile의 3개 StyleChip만
    # AI가 반환할 수 있도록 schema 제한
    response_schema = deepcopy(
        LOOK_RESPONSE_SCHEMA
    )

    response_schema[
        "properties"
    ][
        "looks"
    ][
        "items"
    ][
        "properties"
    ][
        "style_chip"
    ][
        "enum"
    ] = profile_chip_codes

    prompt = f"""
You are an MCM fashion styling assistant.

Create exactly 3 curated looks.

USER STYLE CHIPS:
{json.dumps(profile_chips, ensure_ascii=False)}

REQUIRED MAIN PRODUCT FOR EACH STYLE CHIP:
{json.dumps(required_products_by_chip, ensure_ascii=False)}

OPTIONAL RECENTLY VISITED PRODUCTS:
{json.dumps(optional_product_data, ensure_ascii=False)}

AVAILABLE PRODUCTS:
{json.dumps(product_candidates, ensure_ascii=False)}

Rules:

1. Create exactly one Look for each USER STYLE CHIP.

2. You MUST use each of these style chip codes exactly once:
   {json.dumps(profile_chip_codes, ensure_ascii=False)}

3. Do not use any style chip that is not listed above.

4. Every product listed in REQUIRED MAIN PRODUCT FOR EACH STYLE CHIP
   MUST be included in that Look.

5. The required main product must use:
   "source": "VISITED"

6. OPTIONAL RECENTLY VISITED PRODUCTS may be included
   only when they improve the styling.

7. OPTIONAL RECENTLY VISITED PRODUCTS are not required
   to appear in any Look.

8. If an optional recently visited product is used,
   it must use:
   "source": "VISITED"

9. Products that are not from the visited product lists
   must use:
   "source": "RECOMMENDED"

10. Each Look must contain exactly:
    BAG
    TOP
    BOTTOM
    SHOES
    ACCESSORY

11. Each item type must appear exactly once.

12. Do not include two products of the same category
    in the same Look.

13. Only use product IDs from AVAILABLE PRODUCTS.

14. Recommended products should complement the
    visited products based on color, material,
    pattern, design, and overall style.

15. title must be written in English
    and should be short and stylish.

16. subtitle must be written in English
    and should be concise and natural.

17. description must be written in Korean,
    must be one short sentence,
    and must not exceed 31 characters,
    including spaces and punctuation.

18. reason must be written in Korean,
    must be one short sentence,
    and must not exceed 31 characters,
    including spaces and punctuation.

19. Keep title, subtitle, description, and reason concise and natural.
"""


    response_schema = deepcopy(LOOK_RESPONSE_SCHEMA)

    response_schema["properties"]["looks"]["items"]["properties"]["style_chip"]["enum"] = (
    profile_chip_codes
)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "fashion_looks",
                "schema": response_schema,
                "strict": True,
            }
        },
    )

    data = json.loads(
        response.output_text
    )

    looks = data["looks"]

    # 마지막 안전 검증
    generated_chip_codes = [
        look["style_chip"]
        for look in looks
    ]

    if (
        len(generated_chip_codes) != 3
        or set(generated_chip_codes) != set(profile_chip_codes)
    ):
        raise ValueError(
            "AI Look의 StyleChip 구성이 "
            "StyleProfile의 StyleChip과 일치하지 않습니다."
        )

    return looks

def create_ai_looks(
    style_profile,
    assignments,
    visited_products
):
    # 가장 최근 제품을 제외한
    # 2번째, 3번째 방문 제품
    optional_products = visited_products[1:]

    look_data_list = generate_ai_looks(
        style_profile,
        assignments,
        optional_products
    )

    looks = save_looks(
        style_profile,
        look_data_list,
        visited_products=visited_products
    )

    return looks



# 제품들을 StyleChip에 배치하는 함수
def assign_products_to_style_chips(
    products,
    style_chips
):
    if not products:
        raise ValueError(
            "분석할 방문 제품이 없습니다."
        )

    if len(style_chips) != 3:
        raise ValueError(
            "StyleChip은 정확히 3개여야 합니다."
        )

    main_product = products[0]

    return {
        chip.code: [main_product]
        for chip in style_chips
    }

# def remove_category_duplicates(products):
#     result = []
#     categories = set()

#     for product in products:
#         if product.category in categories:
#             continue

#         result.append(product)
#         categories.add(product.category)

#     return result