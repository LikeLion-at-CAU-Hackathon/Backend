from datetime import datetime, time

from django.core.management.base import BaseCommand
from django.utils import timezone

from products.models import *

leather_careguide = {
    "01": "가죽 제품이 젖거나 얼룩지지 않도록 주의해 주세요.",
    "02": "표면이 젖거나 오염되었을 경우 보풀이 없는 밝은색의 흡수성 천으로 닦아 말려주세요.",
    "03": "제품 표면에 비누나 솔벤트를 사용하지 마세요.",
    "04": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
    "05": "더스트 백에 넣어 직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
}


def seed_product_1():
    # =========================
    # 1. Product
    # =========================

    product = Product.objects.create(
        name="Aren 비세토스 3단 지갑",
        category="지갑",
        specs={
            "dimensions": "약 3 x 12 x 9 cm",
            "closure": "Snap Closure",
            "card_slots": "6 Slots",
            "storage": "Bill Compartment · Zipper Pocket",
        },
        background={
            "description": (
                "헤리티지 하드웨어로 완성한 모노그램 지갑. "
                "비세토스 모노그램 캔버스에 MCM 로고 브라스 플레이트와 "
                "스냅 클로저를 더했습니다. "
                "트라이폴드 구조로 구성된 지갑으로, "
                "아이코닉한 MCM 로고와 헤리티지 하드웨어를 통해 "
                "MCM의 디자인 아이덴티티를 보여줍니다."
            ),
            "collection": "Visetos",
            "design": "Aren 비세토스 3단 지갑",
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    cognac = ProductDetail.objects.create(
        product=product,
        size="S",
        color="Cognac",
        price=490000,
    )

    soft_pink = ProductDetail.objects.create(
        product=product,
        size="S",
        color="Soft Pink",
        price=490000,
    )

    # =========================
    # 3. Material
    # =========================

    visetos = Material.objects.create(
        name="Visetos Monogram Canvas",
        description=(
            "MCM의 시그니처 비세토스 모노그램 캔버스를 바디에 사용했습니다. "
            "클래식한 모노그램 패턴과 헤리티지 하드웨어가 조화를 이루며 "
            "MCM의 아이덴티티를 완성합니다."
        ),
        order=1,
        careguide={
            "01": "지속적인 직사광선을 피해 주세요.",
            "02": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
            "03": "더스트 백에 넣어 직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
            "04": "제품 표면에 비누나 솔벤트를 사용하지 마세요.",
        },
    )

    natural_leather = Material.objects.create(
        name="Natural Leather",
        description=(
            "천연 가죽으로 트림을 마감했습니다. "
            "카드 슬롯과 가장자리 디테일에 가죽 소재가 적용되었습니다."
        ),
        order=2,
        careguide=leather_careguide,
    )

    gold_plated_brass = Material.objects.create(
        name="24K Gold-Plated Brass",
        description=(
            "브라스 하드웨어에 24K 골드 도금을 적용했습니다. "
            "MCM 로고 장식 플레이트와 스냅 클로저에 사용됩니다."
        ),
        order=3,
        careguide={
            "01": "지속적인 직사광선을 피해 주세요.",
            "02": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
            "03": "더스트 백에 넣어 직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
            "04": "제품 표면에 비누나 솔벤트를 사용하지 마세요.",
        },
    )

    fabric_lining = Material.objects.create(
        name="Fabric Lining",
        description="지갑 내부에 패브릭 안감을 적용했습니다.",
        order=4,
        careguide={
            "01": "지속적인 직사광선을 피해 주세요.",
            "02": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
            "03": "더스트 백에 넣어 직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.create(
        material=visetos,
        product=product,
    )

    MaterialProduct.objects.create(
        material=natural_leather,
        product=product,
    )

    MaterialProduct.objects.create(
        material=gold_plated_brass,
        product=product,
    )

    MaterialProduct.objects.create(
        material=fabric_lining,
        product=product,
    )
    
    return product
    
def seed_product_2():
    # =========================
    # 1. Product
    # =========================

    product = Product.objects.create(
        name="모노그램 프린트 뿌띠 실크 스카프",
        category="스카프",
        specs={
            "dimensions": "약 8 x 120 x 0 cm",
            "design": "Reversible",
            "construction": "Hand-Sewn",
            "material": "Organic Silk 100%",
        },
        background={
            "description": (
                "두 가지 아이콘을 담은 리버서블 디자인. "
                "앞면에는 비세토스 모노그램 프린트, "
                "반대쪽 면에는 MCM 로고와 대비되는 스트라이프 컬러 블록 모티프를 "
                "적용했습니다. "
                "하나의 스카프로 두 가지 디자인을 즐길 수 있으며, "
                "스카프·리본 매듭·가방 핸들 등 다양한 방식으로 스타일링할 수 있습니다."
            ),
            "design_details": {
                "01": "MAIN SIDE Visetos Monogram Print",
                "02": "REVERSE SIDE MCM Logo & Contrast Stripe Print",
                "03": "REVERSIBLE 양면 디자인",
                "04": "STYLING 스카프 · 리본 매듭 · 가방 핸들",
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    detail = ProductDetail.objects.create(
        product=product,
        size="Free",
        color="Cognac",
        price=175000,
    )

    # =========================
    # 3. Material
    # =========================

    organic_silk = Material.objects.create(
        name="Organic Silk 100%",
        description=(
            "오가닉 이탈리안 실크 100%를 사용해 가볍고 부드러운 촉감을 완성했습니다. "
            "은은한 광택이 더해져 고급스러운 소재감을 보여줍니다."
        ),
        order=1,
        careguide={
            "01": "드라이클리닝 전용. 스카프는 드라이클리닝으로 관리해 주세요.",
            "02": "물세탁은 피하고 제품의 소재 특성에 맞게 관리해 주세요.",
            "03": "제품과 함께 제공되는 더스트 백에 넣어 직사광선이나 밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요.",
            "04": "젖거나 오염되지 않도록 주의해 주세요.",
            "05": "표면이 젖거나 오염되었을 경우 보풀이 없는 밝은색의 흡수성 천으로 닦아 말려주세요.",
            "06": "비누나 솔벤트를 사용하지 마세요.",
            "07": "거친 표면과의 마찰에 주의해 주세요.",
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.create(
        material=organic_silk,
        product=product,
    )
    
    return product

def seed_product_3():

    # =========================
    # 1. Product
    # =========================

    product = Product.objects.create(
        name="에센셜 로고 프린트 티셔츠",
        category="상의",

        specs={
            "fit": "Regular Fit",
            "design": "Short Sleeve",
            "neckline": "Rib Knit",
            "material": "100% Organic Cotton",

            "size_measurements": {
                "S": {
                    "korean_size": 95,
                    "height": "170 cm",
                    "length": "67.0 cm",
                    "shoulder": "44.0 cm",
                    "sleeve": "22.1 cm",
                    "chest": "96-98 cm",
                },
                "M": {
                    "korean_size": 100,
                    "height": "175 cm",
                    "length": "69.0 cm",
                    "shoulder": "46.0 cm",
                    "sleeve": "22.8 cm",
                    "chest": "108-110 cm",
                },
                "L": {
                    "korean_size": 105,
                    "height": "180 cm",
                    "length": "71.0 cm",
                    "shoulder": "48.0 cm",
                    "sleeve": "23.5 cm",
                    "chest": "118-122 cm",
                },
                "XL": {
                    "korean_size": 110,
                    "height": "185 cm",
                    "length": "73.0 cm",
                    "shoulder": "50.0 cm",
                    "sleeve": "24.2 cm",
                    "chest": "126-130 cm",
                },
            },
        },

        background={
            "description": (
                "메탈릭 로고로 완성한 미니멀한 시그니처. "
                "오가닉 코튼 저지에 시그니처 라우렐 엠블럼을 "
                "메탈릭 하이 프리퀀시 프린트로 담아냈습니다. "
                "심플한 실루엣 위에 MCM의 상징적인 로고를 더해 "
                "절제된 디자인에 감각적인 포인트를 완성했습니다."
            ),

            "design_details": {
                "01": "SIGNATURE Laurel Emblem",
                "02": "LOGO DETAIL Metallic High-Frequency Print",
                "03": "NECKLINE Rib Knit Neckline",
                "04": "FIT Regular Fit",
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = ["Black", "White"]
    sizes = ["S", "M", "L", "XL"]

    for color in colors:
        for size in sizes:
            ProductDetail.objects.create(
                product=product,
                size=size,
                color=color,
                price=270000,
            )

    # =========================
    # 3. Material
    # =========================

    material = Material.objects.create(
        name="Organic Cotton 100%",

        description=(
            "100% 오가닉 코튼 저지 소재를 사용해 "
            "부드럽고 편안한 착용감을 완성했습니다. "
            "일상적인 착용에 적합한 소재입니다."
        ),

        order=1,

        careguide={
            "01": "세탁 또는 드라이클리닝으로 관리해 주세요.",
            "02": "표백제를 사용하지 마세요.",
            "03": "건조기 사용을 피해 주세요.",
            "04": "다림질할 때는 천을 대고 다림질해 주세요.",
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.create(
        material=material,
        product=product,
    )
    
    return product

def seed_product_4():

    # =========================
    # 1. Product
    # =========================

    product = Product.objects.create(
        name="오발 선글라스",
        category="선글라스",

        specs={
            "size": "53-16-145 mm",
            "lens_color": "Solid Smoke",
            "frame_color": "Shiny Black",
            "case": "Logo-Embossed Pouch Case",

            "design_details": {
                "01": "SHAPE Oval",
                "02": "TEMPLE MCM Logo",
                "03": "TEMPLE TIP Bavarian Diamond Metal Stud",
                "04": "STYLE Unisex",
            },
        },

        background={
            "description": (
                "부드러운 곡선으로 완성한 오발 실루엣이 특징인 "
                "타원형 디자인으로 깔끔하고 미니멀한 디자인을 보여줍니다. "
                "템플에는 클래식한 MCM 로고를 더하고, "
                "팁에는 바이예른 다이아몬드 메탈 스터드를 장식했습니다."
            ),

            "materials": {
                "frame": (
                    "아세테이트 프레임내구성과 가벼운 착용감을 갖춘 "
                    "아세테이트 소재로 프레임을 제작했습니다."
                ),
                "lens": (
                    "Solid Smoke Lens솔리드 스모크 컬러의 렌즈를 적용해 "
                    "차분한 시각적 인상을 완성합니다."
                ),
                "hardware": (
                    "Metal Hardware템플에 메탈 소재의 하드웨어 디테일을 적용했습니다."
                ),
                "case": (
                    "Logo-Embossed Pouch Case제품 보관을 위한 "
                    "로고 엠보싱 파우치 케이스가 함께 구성됩니다."
                ),
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = ["Pink", "Black"]

    for color in colors:
        ProductDetail.objects.create(
            product=product,
            size="Free",
            color=color,
            price=260000,
        )

    # =========================
    # 3. Material
    # =========================
    
    sunglasses_careguide = {
        "01": "서늘하고 건조한 곳에 보관하세요.",
        "02": "제품과 함께 제공되는 더스트 백에 넣어 직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
        "03": "제품 표면을 부드럽게 관리해 주세요.",
        "04": "표면이 젖었을 경우 보풀이 없는 밝은색의 흡수성 천으로 물기를 닦아 말려주세요.",
        "05": "비누나 솔벤트를 사용하지 마세요.",
        "06": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
    }

    acetate_frame = Material.objects.create(
        name="Acetate Frame",
        description=(
            "아세테이트 프레임에 내구성과 가벼운 착용감을 갖춘 "
            "아세테이트 소재로 프레임을 제작했습니다."
        ),
        order=1,
        careguide=sunglasses_careguide,
    )

    smoke_lens = Material.objects.create(
        name="Solid Smoke Lens",
        description=(
            "솔리드 스모크 컬러의 렌즈를 적용해 "
            "차분한 시각적 인상을 완성합니다."
        ),
        order=2,
        careguide=sunglasses_careguide,
    )

    metal_hardware = Material.objects.create(
        name="Metal Hardware",
        description=(
            "템플에 메탈 소재의 하드웨어 디테일을 적용했습니다."
        ),
        order=3,
        careguide=sunglasses_careguide,
    )

    pouch_case = Material.objects.create(
        name="Logo-Embossed Pouch Case",
        description=(
            "제품 보관을 위한 로고 엠보싱 파우치 케이스가 "
            "함께 구성됩니다."
        ),
        order=4,
        careguide=sunglasses_careguide,
    )

    # =========================
    # 4. MaterialProduct
    # =========================
    
    for material in [
        acetate_frame,
        smoke_lens,
        metal_hardware,
        pouch_case,
    ]:
        MaterialProduct.objects.create(
            material=material,
            product=product,
        )
        
    return product

def seed_product_5():

    # =========================
    # 1. Product
    # =========================

    product = Product.objects.create(
        name="MCM 오 드 퍼퓸",
        category="향수",

        specs={
            "product_type": "Unisex Fragrance",

            "top_notes": [
                "Raspberry",
                "Apricot",
            ],

            "heart_notes": [
                "Hand-Picked Jasmine",
                "White Peony",
                "Violet Leaf",
            ],

            "base_notes": [
                "White Moss",
                "Vanilla",
                "Sandalwood",
                "Sheer Ambrox",
            ],

            "design_details": {
                "01": "FORM Star Backpack-inspired Bottle",
                "02": "DETAIL Gold-Tone Metal Details",
                "03": "IDENTITY MCM Travel DNA",
                "04": "STYLE Unisex",
            },
        },

        background={
            "description": (
                "MCM의 여행 DNA를 담은 스타크 백팩 보틀. "
                "MCM의 여행 DNA를 표현한 향수 보틀은 "
                "전설적인 스타크 백팩을 모델로 정교하게 제작되었습니다."
            ),

            "materials": {
                "fragrance": (
                    "Fragrance / Parfum "
                    "할로라즈베리, 애프리콧, 재스민, 화이트 피오니, "
                    "바이올렛 리프 등의 향료를 조합했습니다."
                ),

                "alcohol_base": (
                    "Alcohol Base "
                    "SD Alcohol 40-B (Alcohol Denat.)를 베이스로 사용해 "
                    "향이 자연스럽게 퍼지도록 구성했습니다."
                ),

                "purified_water": (
                    "Purified Water "
                    "정제수를 사용해 향료와 베이스 성분의 균형을 맞췄습니다."
                ),

                "additional_ingredients": (
                    "Additional Ingredients "
                    "Butylene Glycol · BHT · Ethylhexyl Methoxycinnamate · "
                    "Ethylhexyl Salicylate · Butyl Methoxydibenzoylmethane"
                ),
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    # 현재 자료에서는 141,000원이라는 가격만 확인됨.
    # 목업 데이터이므로 동일 가격으로 입력.
    # 실제 사이즈별 가격이 확인되면 수정.

    sizes = [
        "10ml",
        "30ml",
        "50ml",
        "75ml",
    ]

    for size in sizes:
        ProductDetail.objects.create(
            product=product,
            size=size,
            color="Cognac",
            price=141000,
        )

    # =========================
    # 3. Material
    # =========================

    material = Material.objects.create(
        name="Fragrance / Parfum",

        description=(
            "할로라즈베리, 애프리콧, 재스민, 화이트 피오니, "
            "바이올렛 리프 등의 향료를 조합했습니다. "
            "SD Alcohol 40-B (Alcohol Denat.)를 베이스로 사용해 "
            "향이 자연스럽게 퍼지도록 구성했습니다. "
            "정제수를 사용해 향료와 베이스 성분의 균형을 맞췄습니다."
        ),

        order=1,

        careguide={
            "01": "USE 피부에 바르는 용도로만 사용하세요.",
            "02": "ALCOHOL 알코올이 포함되어 있습니다.",
            "03": "FIRE 화기 근처에서 사용하지 마세요.",
            "04": (
                "STORAGE 서늘하고 건조한 곳에 보관하세요. "
                "제품과 함께 제공되는 더스트 백에 넣어 직사광선이나 "
                "밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요."
            ),
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.create(
        material=material,
        product=product,
    )
    
    return product

def seed_product_6():

    # =========================
    # 1. Product
    # =========================

    product = Product.objects.create(
        name="클라우스 M 비세토스 리버서블 벨트 4.5cm",
        category="벨트",

        specs={
            "dimensions": "약 0 x 130 x 5 cm",
            "waist_size": "122 cm",
            "design": "Reversible",
            "adjustment": "Length Adjustable",
        },

        background={
            "description": (
                "하나의 벨트로 두 가지 시그니처한 면을 선보이는 "
                "리버서블 디자인입니다. 아이코닉한 M 버클은 탈착이 가능하며, "
                "스트랩을 잘라 원하는 길이로 조절할 수 있습니다."
            ),

            "design_details": {
                "01": "REVERSIBLE Monogram Coated Canvas · Solid Leather",
                "02": "BUCKLE Detachable M Buckle",
                "03": "ADJUSTMENT Cut-to-Length",
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = [
        "Black / Matte Black",
        "Cognac / Gold",
        "Black",
    ]

    for color in colors:
        ProductDetail.objects.create(
            product=product,
            size="Cut to Size",
            color=color,
            price=450000,
        )

    # =========================
    # 3. Material
    # =========================

    coated_canvas = Material.objects.create(
        name="Coated Canvas",
        description=(
            "코티드 캔버스의 내구성을 높인 코팅 캔버스를 사용해 "
            "견고한 표면감과 실용성을 더했습니다."
        ),
        order=1,
        careguide={
            "01": "직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관하세요.",
            "02": "표면에 오염이 생겼을 경우 부드러운 천으로 가볍게 닦아주세요.",
            "03": "비누나 솔벤트를 사용하지 마세요.",
        },
    )

    solid_leather = Material.objects.create(
        name="Solid Leather",
        description=(
            "반대쪽 면에는 솔리드 레더를 사용해 "
            "서로 다른 소재감을 하나의 스트랩에 담았습니다."
        ),
        order=2,
        careguide=leather_careguide,
    )

    nappa_leather_trim = Material.objects.create(
        name="Nappa Leather Trim",
        description=(
            "부드러운 나파 가죽으로 가장자리와 트림을 "
            "섬세하게 마감했습니다."
        ),
        order=3,
        careguide=leather_careguide,
    )

    metal_hardware = Material.objects.create(
        name="Metal Hardware",
        description=(
            "금속 하드웨어를 적용해 구조적인 완성도와 "
            "내구성을 높였습니다."
        ),
        order=4,
        careguide={
            "01": "직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관하세요.",
            "02": "표면을 부드럽게 관리해주세요.",
        },
    )
    
    # =========================
    # 4. MaterialProduct
    # =========================

    for material in [
        coated_canvas,
        solid_leather,
        nappa_leather_trim,
        metal_hardware,
    ]:
        MaterialProduct.objects.create(
            material=material,
            product=product,
        )
        
    return product

def seed_product_7():

    # =========================
    # 1. Product
    # =========================

    product = Product.objects.create(
        name="네오 테리엔 모노그램 레더 로우탑 스니커즈",
        category="신발",

        specs={
            "product_type": "Low-Top Sneakers",
            "upper": "100% Calf Leather",
            "trim": "100% Calf Leather",
            "lining": "Leather Lining with Mesh",
            "insole": "Removable OrthoLite® Memory Foam Insole",
            "outsole": "Rubber Outsole · MCM Logo Motif",
        },

        background={
            "description": (
                "비세토스 모노그램으로 완성한 로우탑 실루엣의 "
                "비세토스 모노그램 스니커즈입니다. "
                "가죽으로 완성된 옆면과 후면, 바이올렛 다이아몬드를 참고한 "
                "루버 패치가 디자인에 포인트를 더합니다."
            ),

            "design_details": {
                "01": "MONOGRAM Embossed Visetos Monogram",
                "02": "TONGUE Laurel Logo Label",
                "03": "HEEL Leather Diamond Patch",
                "04": "OUTSOLE Rubber Outsole · MCM Logo Motif",
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = [
        "36IT",
        "37IT",
        "38IT",
        "39IT",
        "40IT",
        "41IT",
        "42IT",
        "43IT",
    ]

    for size in sizes:
        ProductDetail.objects.create(
            product=product,
            size=size,
            color="Egret",
            price=770000,
        )

    # =========================
    # 3. Material
    # =========================
    
    sneaker_careguide = {
        "01": "향수, 화장품, 오일 및 물과의 접촉을 피하십시오.",
        "02": "클리닝 전에 내부 삽입물을 제거하세요.",
        "03": "클리닝 후 실내 온도에서 건조하세요.",
        "04": "아웃솔은 부드러운 브러시를 사용해 세척하세요.",
        "05": "어퍼는 살짝 물에 적신 코튼 천을 사용해 세척하세요.",
    }

    calf_leather = Material.objects.create(
        name="100% Calf Leather",
        description=(
            "송아지 가죽 어퍼와 트림에 100% 송아지 가죽을 사용해 "
            "부드러운 질감과 견고한 구조를 완성했습니다."
        ),
        order=1,
        careguide=sneaker_careguide,
    )

    leather_mesh_lining = Material.objects.create(
        name="Leather & Mesh Lining",
        description=(
            "가죽과 메쉬를 조합한 안감을 적용해 "
            "편안한 착용감과 통기성을 높였습니다."
        ),
        order=2,
        careguide=sneaker_careguide,
    )

    ortholite = Material.objects.create(
        name="OrthoLite® Memory Foam",
        description=(
            "탈착 가능한 OrthoLite® 메모리폼 인솔을 적용해 "
            "쿠셔닝과 발의 편안함을 강화했습니다."
        ),
        order=3,
        careguide=sneaker_careguide,
    )

    rubber_outsole = Material.objects.create(
        name="Rubber Outsole",
        description=(
            "러버 아웃솔을 사용해 안정적인 접지력과 "
            "내구성을 제공합니다."
        ),
        order=4,
        careguide=sneaker_careguide,
    )
    
    # =========================
    # 4. MaterialProduct
    # =========================

    for material in [
        calf_leather,
        leather_mesh_lining,
        ortholite,
        rubber_outsole,
    ]:
        MaterialProduct.objects.create(
            material=material,
            product=product,
        )
        
    return product



def seed_branches():
    branches = {}

    branch_data = [
        {
            "name": "신세계 면세점 본점",
            "latitude": 37.5603907,
            "longitude": 126.9808854,
            "open": time(11, 0),
            "close": time(18, 0),
        },
        {
            "name": "롯데백화점 본점",
            "latitude": 37.5647299033135,
            "longitude": 126.981730421825,
            "open": time(10, 30),
            "close": time(20, 0),
        },
        {
            "name": "롯데면세점 명동본점",
            "latitude": 37.5653458904198,
            "longitude": 126.9810075639,
            "open": time(9, 30),
            "close": time(20, 0),
        },
        {
            "name": "신라면세점 본점",
            "latitude": 37.5573514,
            "longitude": 127.0075502,
            "open": time(9, 30),
            "close": time(17, 30),
        },
    ]

    for data in branch_data:
        branch = Branch.objects.create(
            name=data["name"],
            latitude=data["latitude"],
            longitude=data["longitude"],
        )

        BusinessHours.objects.create(
            branch=branch,
            open=data["open"],
            close=data["close"],
        )

        branches[data["name"]] = branch

    return branches

def seed_stocks(products, branches):
    stock_data = {
        # =====================================================
        # 1번 Aren 비세토스 3단 지갑
        # =====================================================
        1: {
            "신세계 면세점 본점": 3,
            "롯데백화점 본점": 2,
            "롯데면세점 명동본점": 1,
            "신라면세점 본점": 2,
        },

        # =====================================================
        # 2번 모노그램 프린트 뿌띠 실크 스카프
        # =====================================================
        2: {
            "신세계 면세점 본점": 2,
            "롯데백화점 본점": 1,
            "롯데면세점 명동본점": 3,
            "신라면세점 본점": 1,
        },

        # =====================================================
        # 3번 에센셜 로고 프린트 티셔츠
        # =====================================================
        3: {
            "신세계 면세점 본점": {
                "S": 2,
                "M": 1,
                "L": 0,
                "XL": 1,
            },
            "롯데백화점 본점": {
                "S": 1,
                "M": 2,
                "L": 1,
                "XL": 0,
            },
            "롯데면세점 명동본점": {
                "S": 3,
                "M": 0,
                "L": 1,
                "XL": 2,
            },
            "신라면세점 본점": {
                "S": 1,
                "M": 1,
                "L": 2,
                "XL": 1,
            },
        },

        # =====================================================
        # 4번 오발 선글라스
        # =====================================================
        4: {
            "신세계 면세점 본점": 3,
            "롯데백화점 본점": 2,
            "롯데면세점 명동본점": 1,
            "신라면세점 본점": 2,
        },

        # =====================================================
        # 5번 MCM 오 드 퍼퓸
        # =====================================================
        5: {
            "신세계 면세점 본점": 2,
            "롯데백화점 본점": 1,
            "롯데면세점 명동본점": 2,
            "신라면세점 본점": 1,
        },

        # =====================================================
        # 6번 클라우스 M 비세토스 리버서블 벨트
        # =====================================================
        6: {
            "신세계 면세점 본점": 3,
            "롯데백화점 본점": 2,
            "롯데면세점 명동본점": 1,
            "신라면세점 본점": 2,
        },

        # =====================================================
        # 7번 네오 테리엔 모노그램 레더 로우탑 스니커즈
        # =====================================================
        7: {
            "신세계 면세점 본점": {
                "36IT": 2,
                "37IT": 0,
                "38IT": 1,
                "39IT": 1,
                "40IT": 0,
                "41IT": 2,
                "42IT": 0,
                "43IT": 1,
            },

            "롯데백화점 본점": {
                "36IT": 1,
                "37IT": 1,
                "38IT": 2,
                "39IT": 0,
                "40IT": 1,
                "41IT": 1,
                "42IT": 0,
                "43IT": 2,
            },

            "롯데면세점 명동본점": {
                "36IT": 0,
                "37IT": 1,
                "38IT": 1,
                "39IT": 2,
                "40IT": 0,
                "41IT": 1,
                "42IT": 1,
                "43IT": 0,
            },

            "신라면세점 본점": {
                "36IT": 1,
                "37IT": 0,
                "38IT": 2,
                "39IT": 1,
                "40IT": 0,
                "41IT": 1,
                "42IT": 1,
                "43IT": 0,
            },
        },
    }

    for product_id, branch_data in stock_data.items():

        product = products[product_id - 1]

        for branch_name, stock_info in branch_data.items():

            branch = branches[branch_name]

            for detail in product.details.all():

                # 사이즈별 재고가 있는 경우
                if isinstance(stock_info, dict):
                    quantity = stock_info.get(detail.size, 0)

                # 사이즈가 하나인 제품
                else:
                    quantity = stock_info

                Stock.objects.create(
                    branch=branch,
                    detail=detail,
                    quantity=quantity,
                )




class Command(BaseCommand):
    help = "제품, 지점, 재고 seed 데이터 생성"

    def handle(self, *args, **options):

        Stock.objects.all().delete()
        BusinessHours.objects.all().delete()
        Branch.objects.all().delete()

        MaterialProduct.objects.all().delete()
        ProductDetail.objects.all().delete()
        Material.objects.all().delete()
        Product.objects.all().delete()

        products = [
            seed_product_1(),
            seed_product_2(),
            seed_product_3(),
            seed_product_4(),
            seed_product_5(),
            seed_product_6(),
            seed_product_7(),
        ]

        branches = seed_branches()

        seed_stocks(products, branches)

        self.stdout.write(
            self.style.SUCCESS(
                "제품 1~7 및 지점/영업시간/재고 seed 데이터 생성 완료"
            )
        )