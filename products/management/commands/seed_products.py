from datetime import time

from django.core.management.base import BaseCommand

from products.models import *

leather_careguide = {
    "LEATHER": "가죽 제품이 젖거나 얼룩지지 않도록 주의해 주세요.",
    "CLEANING": "표면이 젖거나 오염되었을 경우 보풀이 없는 밝은색의 흡수성 천으로 닦아 말려주세요.",
    "CAUTION": "제품 표면에 비누나 솔벤트를 사용하지 마세요.",
    "CAUTION": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
    "STORAGE": "더스트 백에 넣어 직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
}

metal_careguide = {
    "METAL": "습기와 물에 장시간 노출되지 않도록 주의해 주세요.",
    "CLEANING": "부드럽고 마른 천으로 표면을 관리해 주세요.",
    "CAUTION": "거친 표면과의 마찰을 피해주세요.",
}


visetos_careguide = {
    "CARE": "지속적인 직사광선을 피해 주세요.",
    "CAUTION": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
    "STORAGE": "더스트 백에 넣어 직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
    "CAUTION": "제품 표면에 비누나 솔벤트를 사용하지 마세요.",
}


fabric_careguide = {
    "CLEANING": "오염 시 부드러운 천으로 가볍게 관리해 주세요.",
    "STORAGE": "습기와 직사광선을 피해 서늘하고 건조한 곳에 보관해 주세요.",
}

COMMON_MATERIALS = {
    "Visetos Monogram Canvas": {
        "description": (
            "MCM의 시그니처 비세토스 모노그램을 적용한 캔버스 소재로, "
            "클래식한 패턴과 견고한 소재감을 특징으로 합니다."
        ),
        "careguide": visetos_careguide,
    },

    "Natural Leather": {
        "description": (
            "천연 가죽 소재로 부드러운 질감과 견고한 마감을 제공합니다."
        ),
        "careguide": leather_careguide,
    },

    "Natural Nappa Leather": {
        "description": (
            "천연 나파 가죽 소재로 부드러운 촉감과 유연한 표면감을 제공합니다."
        ),
        "careguide": leather_careguide,
    },

    "Nappa Leather": {
        "description": (
            "부드럽고 유연한 나파 가죽 소재로 정교하고 고급스러운 마감을 제공합니다."
        ),
        "careguide": leather_careguide,
    },

    "24K Gold-Plated Brass": {
        "description": (
            "브라스 소재의 하드웨어에 24K 골드 도금을 적용해 "
            "고급스러운 금속 디테일을 완성했습니다."
        ),
        "careguide": metal_careguide,
    },

    "24K Gold-Plated Metal": {
        "description": (
            "금속 하드웨어에 24K 골드 도금을 적용해 "
            "고급스러운 장식 디테일을 완성했습니다."
        ),
        "careguide": metal_careguide,
    },

    "Suede-Finish Microfiber": {
        "description": (
            "스웨이드 질감으로 마감한 마이크로파이버 소재로 "
            "부드러운 촉감과 깔끔한 내부 마감을 제공합니다."
        ),
        "careguide": fabric_careguide,
    },

    "Fabric Lining": {
        "description": (
            "내부에 패브릭 안감을 적용해 "
            "깔끔하고 실용적인 내부 공간을 완성했습니다."
        ),
        "careguide": fabric_careguide,
    },

    "Organic Cotton Jersey": {
        "description": (
            "오가닉 코튼을 사용한 저지 소재로 "
            "부드럽고 편안한 착용감을 제공합니다."
        ),
        "careguide": {
            "01": "손세탁 또는 드라이클리닝으로 관리해 주세요.",
            "02": "표백제를 사용하지 마세요.",
            "03": "건조기 사용을 피해주세요.",
            "04": "다림질할 때는 천을 대고 다림질해 주세요.",
        },
    },

    "Metallic Lurex Denim": {
        "description": (
            "메탈릭 루렉스 섬유를 직조한 데님 소재로 "
            "은은한 광택과 독특한 표면감을 제공합니다. "
            "66.2% 코튼, 22.8% 폴리에스터, "
            "11% 금속 코팅 섬유로 구성되어 있습니다."
        ),
        "careguide": {
            "01": "손세탁 또는 드라이클리닝으로 관리해 주세요.",
            "02": "표백제를 사용하지 마세요.",
            "03": "건조기 사용을 피해주세요.",
            "04": "제품의 형태와 디테일이 손상되지 않도록 주의해 주세요.",
        },
    },

    "OrthoLite® Memory Foam": {
        "description": (
            "OrthoLite® 메모리폼 소재를 적용해 "
            "쿠셔닝과 편안한 착화감을 제공합니다."
        ),
        "careguide": {
            "01": "오염 시 부드러운 천으로 가볍게 관리해 주세요.",
            "02": "세척 후에는 실온에서 충분히 건조해 주세요.",
        },
    },

    "Rubber Outsole": {
        "description": (
            "러버 아웃솔을 사용해 안정적인 접지력과 내구성을 제공합니다."
        ),
        "careguide": {
            "01": "부드러운 브러시를 사용해 표면을 관리해 주세요.",
            "02": "세척 후에는 실온에서 충분히 건조해 주세요.",
        },
    },

    "Italian Calfskin Leather": {
        "description": (
            "이탈리아산 카프스킨 가죽으로 "
            "부드러운 질감과 견고한 구조감을 제공합니다."
        ),
        "careguide": leather_careguide,
    },

    "Gold-Tone Metal Hardware": {
        "description": (
            "골드톤 메탈 하드웨어를 적용해 "
            "고급스럽고 구조적인 금속 디테일을 완성했습니다."
        ),
        "careguide": metal_careguide,
    },

    "Cobalt Brass Hardware": {
        "description": (
            "코발트 브라스 하드웨어를 사용해 "
            "세련된 금속 장식과 구조적인 디테일을 완성했습니다."
        ),
        "careguide": metal_careguide,
    },
}

def get_common_material(name, order):
    data = COMMON_MATERIALS[name]

    material, _ = Material.objects.update_or_create(
        name=name,
        defaults={
            "description": data["description"],
            "order": order,
            "careguide": data["careguide"],
        },
    )

    return material

def connect_materials(product, materials):
    for material in materials:
        MaterialProduct.objects.get_or_create(
            material=material,
            product=product,
        )


def seed_product_1():
    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="Aren 비세토스 3단 지갑",
        defaults={
            "category": Product.Category.ACCESSORY,
            "specs": {
                "dimensions": "약 3 x 12 x 9 cm",
                "closure": "Snap Closure",
                "card_slots": "6 Slots",
                "storage": "Bill Compartment · Zipper Pocket",
            },
            "background": {
                "description": (
                    "헤리티지 하드웨어를 더한 모노그램 지갑입니다. "
                    "비세토스 모노그램 캔버스에 MCM 로고 브라스 플레이트와 "
                    "스냅 클로저를 더했습니다. "
                    "트라이폴드 구조로 구성된 지갑으로, "
                    "아이코닉한 MCM 로고와 헤리티지 하드웨어를 통해 "
                    "MCM의 디자인 아이덴티티를 보여줍니다."
                ),
                "design_details": {
                    "VISETOS MONOGRAM": "비세토스 모노그램 캔버스",
                    "LOGO BRASS PLATE MCM": "로고 브라스 장식 플레이트",
                    "SNAP CLOSURE": "스냅 클로저",
                    "TRI-FOLD": "트라이폴드 구조",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    cognac, _ = ProductDetail.objects.update_or_create(
        product=product,
        size="S",
        color="Cognac",
        defaults={
            "price": 490000,
        },
    )

    soft_pink, _ = ProductDetail.objects.update_or_create(
        product=product,
        size="S",
        color="Soft Pink",
        defaults={
            "price": 490000,
        },
    )

    # =========================
    # 3. Material
    # =========================

    visetos = get_common_material(
        "Visetos Monogram Canvas",
        order=1,
    )

    natural_leather = get_common_material(
        "Natural Leather",
        order=2,
    )

    gold_plated_brass = get_common_material(
        "24K Gold-Plated Brass",
        order=3,
    )

    fabric_lining = get_common_material(
        "Fabric Lining",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos,
            natural_leather,
            gold_plated_brass,
            fabric_lining,
        ],
    )
    
    return product
    
def seed_product_2():
    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="모노그램 프린트 뿌띠 실크 스카프",
        defaults={
            "category": Product.Category.ACCESSORY,
            "specs": {
                "dimensions": "약 8 x 120 x 0 cm",
                "design": "Reversible",
                "construction": "Hand-Sewn",
                "material": "Organic Silk 100%",
            },
            "background": {
                "description": (
                    "두 가지 아이콘을 담은 리버서블 디자인. "
                    "앞면에는 비세토스 모노그램 프린트, "
                    "반대쪽 면에는 MCM 로고와 대비되는 스트라이프 컬러 블록 모티프를 "
                    "적용했습니다. "
                    "하나의 스카프로 두 가지 디자인을 즐길 수 있으며, "
                    "스카프·리본 매듭·가방 핸들 등 다양한 방식으로 스타일링할 수 있습니다."
                ),
                "design_details": {
                    "MAIN SIDE": "Visetos Monogram Print",
                    "REVERSE SIDE": "MCM Logo & Contrast Stripe Print",
                    "REVERSIBLE": "양면 디자인",
                    "STYLING": "스카프 · 리본 매듭 · 가방 핸들",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    detail, _ = ProductDetail.objects.update_or_create(
        product=product,
        size="Free",
        color="Cognac",
        defaults={
            "price": 175000,
        },
    )

    # =========================
    # 3. Material
    # =========================

    organic_silk, _ = Material.objects.update_or_create(
        name="Organic Silk 100%",
        defaults={
            "description": "오가닉 이탈리안 실크 100%를 사용해 가볍고 부드러운 촉감을 완성했습니다. "
            "은은한 광택이 더해져 고급스러운 소재감을 보여줍니다.",
            "order": 1,
            "careguide": {
                "01": "드라이클리닝 전용. 스카프는 드라이클리닝으로만 관리해 주세요.",
                "02": "물세탁은 피하고 제품의 소재 특성에 맞는 방식으로 관리해 주세요.",
                "03": "제공된 보호용 더스트 백에 넣어 직사광선이나 밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요.",
                "04": "제품이 젖거나 오염되지 않도록 주의해 주세요.",
                "05": "표면이 젖거나 오염되었을 경우 보풀이 없는 밝은 색상의 흡수성 천으로 닦아 말려주세요.",
                "06": "비누 또는 솔벤트를 사용하지 마세요.",
                "07": "제품이 거친 표면에 긁히거나 마찰되지 않도록 주의해 주세요.",
            },
        },
    )

    hand_sewn, _ = Material.objects.update_or_create(
        name="Hand-Sewn Construction",
        defaults={
            "description": "가장자리와 마감 부분을 수작업으로 봉제해 섬세하게 완성했습니다.",
            "order": 2,
            "careguide": {
                "01": "드라이클리닝 전용. 제품의 형태와 섬세한 봉제 상태를 고려하여 관리해 주세요.",
                "02": "물세탁은 피하고 소재의 특성에 맞는 방식으로 관리해 주세요.",
                "03": "보관 시 제품이 눌리거나 접힌 상태로 장시간 방치되지 않도록 주의해 주세요.",
                "04": "봉제된 가장자리와 마감 부분이 거친 표면에 걸리거나 긁히지 않도록 주의해 주세요.",
                "05": "실밥이 풀리거나 봉제 부분이 손상되지 않도록 강한 마찰을 피해주세요.",
                "06": "오염이 발생한 경우 직접 세척하기보다 전문적인 클리닝을 권장합니다.",
                "07": "직사광선이나 밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요.",
            },
        },
    )

    silk_finish, _ = Material.objects.update_or_create(
        name="Silk Finish",
        defaults={
            "description": "실크 특유의 매끄러운 표면감과 자연스러운 드레이프를 살렸습니다.",
            "order": 3,
            "careguide": {
                "01": "드라이클리닝 전용. 실크 특유의 표면감을 유지할 수 있도록 관리해 주세요.",
                "02": "물세탁은 피하고 제품의 소재 특성에 맞는 방식으로 관리해 주세요.",
                "03": "표면에 얼룩이나 오염이 생겼을 경우 강하게 문지르지 마세요.",
                "04": "표면이 젖거나 오염되었을 경우 보풀이 없는 밝은 색상의 흡수성 천으로 닦아 말려주세요.",
                "05": "비누나 솔벤트를 사용하지 마세요.",
                "06": "거친 표면과의 마찰을 피하고 제품 표면이 긁히지 않도록 주의해 주세요.",
                "07": "직사광선이나 밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요.",
            },
        },
    )

    lightweight_fabric, _ = Material.objects.update_or_create(
        name="Lightweight Fabric",
        defaults={
            "description": "가볍고 유연한 소재로 다양한 스타일링에 편안하게 활용할 수 있습니다.",
            "order": 4,
            "careguide": {
                "01": "드라이클리닝 전용. 가벼운 소재의 형태를 유지할 수 있도록 관리해 주세요.",
                "02": "물세탁은 피하고 제품의 소재 특성에 맞는 방식으로 관리해 주세요.",
                "03": "강한 마찰이나 거친 표면과의 접촉을 피해주세요.",
                "04": "제품이 젖거나 오염되지 않도록 주의해 주세요.",
                "05": "표면이 젖거나 오염되었을 경우 보풀이 없는 밝은 색상의 흡수성 천으로 닦아 말려주세요.",
                "06": "비누 또는 솔벤트를 사용하지 마세요.",
                "07": "제공된 보호용 더스트 백에 넣어 직사광선이나 밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            organic_silk,
            hand_sewn,
            silk_finish,
            lightweight_fabric,
        ],
    )

    return product

def seed_product_3():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="에센셜 로고 프린트 티셔츠",
        defaults={
            "category": Product.Category.TOP,
            "specs": {
                "fit": "Regular Fit",
                "design": "Short Sleeve",
                "neckline": "Rib Knit",
                "material": "100% Organic Cotton",
    
                "size_measurements": {
                    "S": {
                        "한국 사이즈": 95,
                        "신장": "170 cm",
                        "길이": "67.0 cm",
                        "어깨": "44.0 cm",
                        "소매": "22.1 cm",
                        "가슴둘레": "96-98 cm",
                    },
                    "M": {
                        "한국 사이즈": 100,
                        "신장": "175 cm",
                        "길이": "69.0 cm",
                        "어깨": "46.0 cm",
                        "소매": "22.8 cm",
                        "가슴둘레": "108-110 cm",
                    },
                    "L": {
                        "한국 사이즈": 105,
                        "신장": "180 cm",
                        "길이": "71.0 cm",
                        "어깨": "48.0 cm",
                        "소매": "23.5 cm",
                        "가슴둘레": "118-122 cm",
                    },
                    "XL": {
                        "한국 사이즈": 110,
                        "신장": "185 cm",
                        "길이": "73.0 cm",
                        "어깨": "50.0 cm",
                        "소매": "24.2 cm",
                        "가슴둘레": "126-130 cm",
                    },
                },
            },
            "background": {
                "description": (
                    "메탈릭 로고로 완성한 미니멀한 시그니처. "
                    "오가닉 코튼 저지에 시그니처 라우렐 엠블럼을 "
                    "메탈릭 하이 프리퀀시 프린트로 담아냈습니다. "
                    "심플한 실루엣 위에 MCM의 상징적인 로고를 더해 "
                    "절제된 디자인에 감각적인 포인트를 완성했습니다."
                ),
    
                "design_details": {
                    "SIGNATURE": "Laurel Emblem",
                    "LOGO DETAIL": "Metallic High-Frequency Print",
                    "NECKLINE": "Rib Knit Neckline",
                    "FIT": "Regular Fit",
                },
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
            ProductDetail.objects.update_or_create(
                product=product,
                size=size,
                color=color,
                defaults={
                    "price": 270000,
                },
            )

    # =========================
    # 3. Material
    # =========================

    organic_cotton, _ = Material.objects.update_or_create(
        name="Organic Cotton 100%",
        defaults={
            "description": "100% 오가닉 코튼 저지 소재를 사용해 "
            "부드럽고 편안한 착용감을 완성했습니다.",
            "order": 1,
            "careguide": {
                "01": "세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 피해 주세요.",
                "04": "다림질할 때는 천을 대고 다림질해 주세요.",
            },
        },
    )

    cotton_jersey, _ = Material.objects.update_or_create(
        name="Cotton Jersey",
        defaults={
            "description": "일상적인 착용에 적합한 부드러운 코튼 저지 소재를 사용했습니다.",
            "order": 2,
            "careguide": {
                "01": "세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 피해 주세요.",
                "04": "다림질할 때는 천을 대고 다림질해 주세요.",
            },
        },
    )

    rib_knit, _ = Material.objects.update_or_create(
        name="Rib Knit",
        defaults={
            "description": "넥라인에 탄탄한 리브 니트 소재를 적용해 형태를 안정적으로 유지합니다.",
            "order": 3,
            "careguide": {
                "01": "세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 피해 주세요.",
                "04": "다림질할 때는 천을 대고 다림질해 주세요.",
            },
        },
    )

    regular_construction, _ = Material.objects.update_or_create(
        name="Regular Construction",
        defaults={
            "description": "여유 있는 기본 구조로 제작해 편안한 데일리 착용감을 제공합니다.",
            "order": 4,
            "careguide": {
                "01": "세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 피해 주세요.",
                "04": "다림질할 때는 천을 대고 다림질해 주세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            organic_cotton,
            cotton_jersey,
            rib_knit,
            regular_construction,
        ],
    )

    return product

def seed_product_4():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="오발 선글라스",
        defaults={
            "category": Product.Category.ACCESSORY,
            "specs": {
                "size": "53-16-145 mm",
                "lens_color": "Solid Smoke",
                "frame_color": "Shiny Black",
                "case": "Logo-Embossed Pouch Case",
    
                "design_details": {
                    "SHAPE": "Oval",
                    "TEMPLE": "MCM Logo",
                    "TEMPLE TIP": "Bavarian Diamond Metal Stud",
                    "STYLE": "Unisex",
                },
            },
            "background": {
                "description": (
                    "부드러운 곡선의 오발 실루엣이 돋보이는 미니멀한 선글라스입니다. "
                    "템플에는 클래식한 MCM 로고를 적용하고, "
                    "템플 팁에는 바이에른 다이아몬드에서 영감을 받은 "
                    "메탈 스터드를 더해 시그니처 디테일을 완성했습니다."
                ),
            }
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = ["Pink", "Black"]

    for color in colors:
        ProductDetail.objects.update_or_create(
            product=product,
            size="Free",
            color=color,
            defaults={
                "price": 260000,
            },
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


    acetate_frame, _ = Material.objects.update_or_create(
        name="Acetate Frame",
        defaults={
            "description": (
                "내구성과 가벼운 착용감을 갖춘 아세테이트 소재로 "
                "프레임을 제작했습니다."
            ),
            "order": 1,
            "careguide": sunglasses_careguide,
        },
    )


    smoke_lens, _ = Material.objects.update_or_create(
        name="Solid Smoke Lens",
        defaults={
            "description": (
                "솔리드 스모크 컬러의 렌즈를 적용해 "
                "차분한 시각적 인상을 완성합니다."
            ),
            "order": 2,
            "careguide": sunglasses_careguide,
        },
    )


    metal_hardware, _ = Material.objects.update_or_create(
        name="Metal Hardware",
        defaults={
            "description": "템플에 메탈 소재의 하드웨어 디테일을 적용했습니다.",
            "order": 3,
            "careguide": sunglasses_careguide,
        },
    )


    logo_embossed_pouch_case, _ = Material.objects.update_or_create(
        name="Logo-Embossed Pouch Case",
        defaults={
            "description": (
                "제품 보관을 위한 로고 엠보싱 파우치 케이스가 "
                "함께 구성됩니다."
            ),
            "order": 4,
            "careguide": sunglasses_careguide,
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================
    
    connect_materials(
        product,
        [
            acetate_frame,
            smoke_lens,
            metal_hardware,
            logo_embossed_pouch_case,
        ],
    )

    return product

def seed_product_5():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="MCM 오 드 퍼퓸",
        defaults={
            "category": Product.Category.ACCESSORY,
            "specs": {
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
            },

            "background": {
                "description": (
                    "MCM의 여행 DNA와 아이코닉한 스타크 백팩에서 영감을 받은 "
                    "유니섹스 오 드 퍼퓸입니다. "
                    "스타크 백팩의 실루엣을 재해석한 보틀에 골드 톤 메탈 디테일을 더해 "
                    "MCM의 브랜드 아이덴티티를 담았습니다."
                ),
                
                "design_details": {
                    "FORM": "Star Backpack-inspired Bottle",
                    "DETAIL": "Gold-Tone Metal Details",
                    "IDENTITY": "MCM Travel DNA",
                    "STYLE": "Unisex",
                },

                "materials": {
                    "fragrance": (
                        "Fragrance / Parfum "
                        "라즈베리, 애프리콧, 재스민, 화이트 피오니, "
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
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Cognac",
            defaults={
                "price": 141000,
            },
        )
        
    # =========================
    # 3. Material
    # =========================

    fragrance_careguide = {
        "01": "USE 피부에 바르는 용도로만 사용하세요.",
        "02": "ALCOHOL 알코올이 포함되어 있습니다.",
        "03": "FIRE 화기 근처에서 사용하지 마세요.",
        "04": (
            "STORAGE 서늘하고 건조한 곳에 보관하세요. "
            "제품과 함께 제공되는 더스트 백에 넣어 직사광선이나 "
            "밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요."
        ),
    }

    fragrance, _ = Material.objects.update_or_create(
        name="Fragrance / Parfum",
        defaults={
            "description": (
                "라즈베리, 애프리콧, 재스민, 화이트 피오니, "
                "바이올렛 리프 등의 향료를 조합했습니다."
            ),
            "order": 1,
            "careguide": fragrance_careguide,
        },
    )

    alcohol_base, _ = Material.objects.update_or_create(
        name="Alcohol Base",
        defaults={
            "description": (
                "SD Alcohol 40-B (Alcohol Denat.)를 베이스로 사용해 "
                "향이 자연스럽게 퍼지도록 구성했습니다."
            ),
            "order": 2,
            "careguide": fragrance_careguide,
        },
    )

    purified_water, _ = Material.objects.update_or_create(
        name="Purified Water",
        defaults={
            "description": (
                "정제수를 사용해 향료와 베이스 성분의 균형을 맞췄습니다."
            ),
            "order": 3,
            "careguide": fragrance_careguide,
        },
    )

    additional_ingredients, _ = Material.objects.update_or_create(
        name="Additional Ingredients",
        defaults={
            "description": (
                "Butylene Glycol · BHT · Ethylhexyl Methoxycinnamate · "
                "Ethylhexyl Salicylate · Butyl Methoxydibenzoylmethane "
                "등을 포함합니다."
            ),
            "order": 4,
            "careguide": fragrance_careguide,
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            fragrance,
            alcohol_base,
            purified_water,
            additional_ingredients,
        ],
    )

    return product

def seed_product_6():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="클라우스 M 비세토스 리버서블 벨트 4.5cm",
        defaults={
            "category": Product.Category.ACCESSORY,
            "specs": {
                "dimensions": "약 0 x 130 x 5 cm",
                "waist_size": "122 cm",
                "design": "Reversible",
                "adjustment": "Length Adjustable",
            },
            "background": {
                "description": (
                    "하나의 벨트로 두 가지 시그니처한 면을 선보이는 디자인. "
                    "한쪽 면은 시그니처 모노그램 코티드 캔버스, "
                    "다른 한쪽은 솔리드 레더로 구성된 리버서블 벨트입니다. "
                    "아이코닉한 M 버클은 탈착이 가능하며, "
                    "스트랩을 잘라 원하는 길이로 조절할 수 있습니다."
                ),
                "design_details": {
                    "REVERSIBLE": "Monogram Coated Canvas · Solid Leather",
                    "BUCKLE": "Detachable M Buckle",
                    "ADJUSTMENT": "Cut-to-Length",
                },
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
        ProductDetail.objects.update_or_create(
            product=product,
            size="Cut to Size",
            color=color,
            defaults={
                "price": 450000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    coated_canvas, _ = Material.objects.update_or_create(
        name="Coated Canvas",
        defaults={
            "description": "코티드 캔버스의 내구성을 높인 코팅 캔버스를 사용해 "
                "견고한 표면감과 실용성을 더했습니다.",
            "order": 1,
            "careguide": {
                "01": "직사광선이나 밝은 빛을 피해 서늘하고 건조한 곳에 보관하세요.",
                "02": "표면에 오염이 생겼을 경우 부드러운 천으로 가볍게 닦아주세요.",
                "03": "비누나 솔벤트를 사용하지 마세요.",
            },
        },
    )

    solid_leather, _ = Material.objects.update_or_create(
        name="Solid Leather",
        defaults={
            "description": "반대쪽 면에는 솔리드 레더를 사용해 "
                "서로 다른 소재감을 하나의 스트랩에 담았습니다.",
            "order": 2,
            "careguide": leather_careguide,
        },
    )

    nappa_leather_trim, _ = Material.objects.update_or_create(
        name="Nappa Leather Trim",
        defaults={
            "description": "부드러운 나파 가죽으로 가장자리와 트림을 "
                "섬세하게 마감했습니다.",
            "order": 3,
            "careguide": leather_careguide,
        },
    )

    metal_hardware, _ = Material.objects.update_or_create(
        name="M Buckle Metal Hardware",
        defaults={
            "description": (
                "금속 하드웨어를 사용해 제품에 구조적인 디테일과 "
                "내구성을 더했습니다."
            ),
            "order": 4,
            "careguide": metal_careguide,
        },
    )
    
    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            coated_canvas,
            solid_leather,
            nappa_leather_trim,
            metal_hardware,
        ],
    )

    return product

def seed_product_7():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="네오 테리엔 모노그램 레더 로우탑 스니커즈",
        defaults={
            "category": Product.Category.SHOES,
            "specs": {
                "product_type": "Low-Top Sneakers",
                "upper": "100% Calf Leather",
                "trim": "100% Calf Leather",
                "lining": "Leather Lining with Mesh",
                "insole": "Removable OrthoLite® Memory Foam Insole",
                "outsole": "Rubber Outsole · MCM Logo Motif",
            },
            "background": {
                "description": (
                    "클래식한 비세토스 모노그램을 새긴 "
                    "이탈리안 송아지 가죽 어퍼로 완성한 로우탑 스니커즈입니다. "
                    "바이에른 다이아몬드에서 영감을 받은 우븐 텅 라벨과 "
                    "가죽 힐 패치가 디자인에 포인트를 더합니다."
                ),
                "design_details": {
                    "MONOGRAM": "Embossed Visetos Monogram",
                    "TONGUE": "Laurel Logo Label",
                    "HEEL": "Leather Diamond Patch",
                    "OUTSOLE": "Rubber Outsole · MCM Logo Motif",
                },
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
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Egret",
            defaults={
                "price": 770000,
            },
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

    calf_leather, _ = Material.objects.update_or_create(
        name="100% Calf Leather",
        defaults={
            "description": (
                "송아지 가죽 어퍼와 트림에 100% 송아지 가죽을 사용해 "
                "부드러운 질감과 견고한 구조를 완성했습니다."
            ),
            "order": 1,
            "careguide": sneaker_careguide,
        },
    )

    leather_mesh_lining, _ = Material.objects.update_or_create(
        name="Leather & Mesh Lining",
        defaults={
            "description": (
                "가죽과 메쉬를 조합한 안감을 적용해 "
                "편안한 착용감과 통기성을 높였습니다."
            ),
            "order": 2,
            "careguide": sneaker_careguide,
        },
    )

    ortholite = get_common_material(
        "OrthoLite® Memory Foam",
        order=3,
    )

    rubber_outsole = get_common_material(
        "Rubber Outsole",
        order=4,
    )
    
    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            calf_leather,
            leather_mesh_lining,
            ortholite,
            rubber_outsole,
        ],
    )
    
    return product


def seed_product_8():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="모노그램 프린트 트라이엥글 실크 스카프",
        defaults={
            "category": Product.Category.ACCESSORY,
            "specs": {
                "dimensions": "약 70 x 70 x 0 cm",
                "material": "100% Silk",
                "pattern": "Visetos Monogram Print · MCM Logo Stripe Motif",
                "shape": "Triangular Silhouette",
            },
            "background": {
                "description": (
                    "뮌헨 하우스의 새로운 실루엣을 제안하는 실크 스카프입니다. "
                    "비세토스 모노그램과 MCM 로고 모티프를 조화롭게 배치해 "
                    "브랜드의 아이덴티티를 표현했습니다. "
                    "삼각형 실루엣과 스트라이프 테두리가 어우러져 "
                    "다양한 스타일링에 활용할 수 있는 디자인을 완성합니다."
                ),

                "design_details": {
                    "SILHOUETTE": "Triangular Shape",
                    "PATTERN": "Visetos Monogram",
                    "BORDER": "MCM Logo & Stripe",
                    "STYLING": "Scarf · Ribbon · Bag Handle",
                },

                "material_details": {
                    "MATERIAL": "100% Silk",
                    "TEXTURE": "Soft & Smooth",
                    "FINISH": "Lightweight & Drapey",
                    "CRAFT": "Fine Edge Finish",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = [
        "Cognac",
        "Soft Pink",
    ]

    for color in colors:
        ProductDetail.objects.update_or_create(
            product=product,
            size="Free",
            color=color,
            defaults={
                "price": 390000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    italian_silk, _ = Material.objects.update_or_create(
        name="100% Italian Silk",
        defaults={
            "description": (
                "100% 이탈리아 실크를 사용해 부드러운 촉감과 "
                "은은한 광택을 완성했습니다. "
                "가볍고 유연한 소재감이 자연스러운 드레이프를 만들어 "
                "다양한 연출이 가능합니다."
            ),
            "order": 1,
            "careguide": {
                "CARE": (
                    "드라이클리닝 전용. 스카프는 드라이클리닝으로만 "
                    "관리해 주세요."
                ),
                "CLEANING": (
                    "물세탁은 피하고 제품의 소재 특성에 맞는 방식으로 "
                    "관리하는 것을 권장합니다."
                ),
                "STORAGE": (
                    "제공된 보호용 더스트 백에 넣어 직사광선이나 "
                    "밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요."
                ),
                "CAUTION": "제품이 젖거나 오염되지 않도록 주의해 주세요.",
                "CLEANING": (
                    "표면이 젖거나 오염되었을 경우 보풀이 없는 "
                    "밝은 색상의 흡수성 천으로 닦아 말려주세요."
                ),
                "CAUTION": "비누 또는 솔벤트를 사용하지 마세요.",
                "CAUTION": (
                    "제품이 거친 표면에 긁히거나 마찰되지 않도록 "
                    "주의해 주세요."
                ),
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================
    
    connect_materials(
        product,
        [
            italian_silk,
        ],
    )

    return product

def seed_product_9():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="Aren 비세토스 호보",
        defaults={
            "category": Product.Category.BAG,
            "specs": {
                "dimensions": {
                    "S": "약 10 x 26 x 19 cm",
                    "L": "약 11 x 34 x 33 cm",
                },
                "closure": "Zip Closure",
                "strap": {
                    "S": "Adjustable Leather Shoulder Strap, 125–133 cm",
                    "L": "Adjustable Leather Shoulder Strap, 92.5–116.5 cm",
                },
                "storage": {
                    "S": "Tablet · Mobile Phone · AirPods · AirPods Max",
                    "L": "Laptop · Tablet · AirPods Max · Tumbler",
                },
            },
            "background": {
                "description": (
                    "클래식한 호보 실루엣을 현대적으로 재해석한 Aren Hobo In Visetos. "
                    "부드러움과 구조감의 이상적인 균형을 보여주는 디자인입니다. "
                    "MCM 헤리티지 러기지에서 가져온 디자인 요소인 탈부착 가능한 "
                    "가죽 행택과 로고가 각인된 패드락을 더해 Aren Hobo만의 "
                    "디자인을 완성했습니다. "
                    "조절 가능한 가죽 스트랩이 적용된 비세토스 호보백으로, "
                    "클래식한 실루엣과 MCM의 헤리티지 러기지 디테일을 "
                    "현대적으로 담아낸 제품입니다."
                ),
                "design_details": {
                    "COLLECTION": "Visetos Collection",
                    "DESIGN": "Softness & Structure",
                    "SIGNATURE": "Leather Hang Tag",
                    "HERITAGE": "MCM Luggage",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = [
        "Cognac",
        "Soft Pink",
        "Black",
    ]

    prices = {
        "S": 1290000,
        "L": 1450000,
    }

    for color in colors:
        for size, price in prices.items():
            ProductDetail.objects.update_or_create(
                product=product,
                size=size,
                color=color,
                defaults={
                    "price": price,
                },
            )

    # =========================
    # 3. Material
    # =========================

    visetos = get_common_material(
        "Visetos Monogram Canvas",
        order=1,
    )

    nappa_leather = get_common_material(
        "Natural Nappa Leather",
        order=2,
    )

    gold_plated_brass = get_common_material(
        "24K Gold-Plated Brass",
        order=3,
    )

    suede_microfiber = get_common_material(
        "Suede-Finish Microfiber",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos,
            nappa_leather,
            gold_plated_brass,
            suede_microfiber,
        ],
    )
    
    return product

def seed_product_10():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="모노그램 크롭 티셔츠",
        defaults={
            "category": Product.Category.TOP,
            "specs": {
                "fit": "Slim Fit",
                "length": "Cropped Length",
                "material": "100% Organic Cotton",
                "model": "173 cm · Wearing Size S",
                "size_measurements": {
                    "S": {
                        "한국 사이즈": 55,
                        "신장": "165–170 cm",
                        "가슴둘레": "84–86 cm",
                    },
                    "M": {
                        "한국 사이즈": 66,
                        "신장": "167–172 cm",
                        "가슴둘레": "92–96 cm",
                    },
                    "L": {
                        "한국 사이즈": 77,
                        "신장": "168–173 cm",
                        "가슴둘레": "98–102 cm",
                    },
                },
            },
            "background": {
                "description": (
                    "밑단에 비세토스 모노그램 자카드 신축성 밴드로 포인트를 준 "
                    "크롭 길이의 오가닉 코튼 티셔츠입니다. "
                    "하우스의 시그니처인 라우렐 엠블럼은 가슴 부분에 "
                    "톤온톤 자수로 표현해 절제된 브랜드 아이덴티티를 완성합니다. "
                    "크롭 기장의 슬림핏 실루엣과 밑단의 자카드 밴드가 조화를 이루어 "
                    "깔끔하면서도 개성 있는 스타일을 보여줍니다."
                ),
                "design_details": {
                    "SIGNATURE": "Tone-on-Tone Laurel Logo",
                    "DETAIL": "Visetos Jacquard Elastic",
                    "SILHOUETTE": "Cropped Length",
                    "FIT": "Slim Fit",
                },
                "material_details": {
                    "BODY": "100% Organic Cotton",
                    "FABRIC": "Cotton Jersey",
                    "ELASTIC": "Visetos Monogram Jacquard Elastic",
                    "EMBROIDERY": "Tone-on-Tone Laurel Logo Embroidery",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = [
        "S",
        "M",
        "L",
    ]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="White",
            defaults={
                "price": 390000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    organic_cotton_jersey = get_common_material(
        "Organic Cotton Jersey",
        order=1,
    )



    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [organic_cotton_jersey],
    )
    
    return product

def seed_product_11():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="루렉스 데님 플레어 팬츠",
        defaults={
            "category": Product.Category.BOTTOM,
            "specs": {
                "fit": "Slim Fit",
                "style": "Flared Denim Pants",
                "pocket": "5-Pocket Style · Silicon Logo Plate Patch",
                "hardware": "Logo-Engraved Metal Buttons · Diamond Studs",
            },
            "background": {
                "description": (
                    "70년대와 디스코 문화에서 영감을 받은 플레어 데님 팬츠로, "
                    "슬림한 실루엣에서 자연스럽게 퍼지는 플레어 라인이 특징입니다. "
                    "5포켓 스타일을 바탕으로 비세토스 모노그램 패치와 "
                    "실리콘 로고 플레이트 패치를 더해 "
                    "MCM의 시그니처 아이덴티티를 표현했습니다."
                ),
                "design_details": {
                    "SILHOUETTE": "Flared Silhouette",
                    "POCKET": "5-Pocket Style",
                    "BACK DETAIL": "Visetos Monogram Patch",
                    "LOGO DETAIL": "Silicon Logo Plate Patch",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = ["38IT", "40IT", "42IT"]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Indigo",
            defaults={
                "price": 830000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    metallic_lurex_denim = get_common_material(
        "Metallic Lurex Denim",
        order=1,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [metallic_lurex_denim],
    )
    
    return product

def seed_product_12():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="모노그램 플랫폼 양가죽 샌들",
        defaults={
            "category": Product.Category.SHOES,
            "specs": {
                "upper": "Lambskin Leather · Visetos Monogram Print",
                "sole": "EVA Platform Sole",
                "strap": "Back Leather Buckle Strap",
                "hardware": "Gold-Tone Bavarian Diamond Metal Buckle",
            },
            "background": {
                "description": (
                    "비세토스 모노그램을 프린트한 크로스 스트랩과 "
                    "플랫폼 실루엣이 조화를 이루는 샌들입니다. "
                    "부드러운 램스킨 풋베드와 버클 스트랩을 더해 "
                    "편안한 착용감을 제공합니다. "
                    "MCM의 시그니처 모노그램과 바이에른 다이아몬드에서 "
                    "영감을 받은 메탈 디테일을 현대적으로 재해석했습니다."
                ),
                "collection": "Visetos Collection",
                "design_details": {
                    "DESIGN": "Platform Sandal",
                    "SIGNATURE": "Visetos Monogram",
                    "HERITAGE": "Bavarian Diamond",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = ["36IT", "37IT", "38IT", "39IT"]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Cognac",
            defaults={
                "price": 890000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    footwear_careguide = {
        "01": "직사광선, 화기 및 습기를 피해 보관해 주세요.",
        "02": "아웃솔은 부드러운 브러시로 관리해 주세요.",
        "03": "어퍼는 살짝 적신 부드러운 면 천으로 닦아주세요.",
        "04": "물, 알코올, 향수, 화장품 및 오일과의 접촉을 피해 주세요.",
    }

    lambskin_leather, _ = Material.objects.update_or_create(
        name="Lambskin Leather",
        defaults={
            "description": (
                "부드러운 양가죽을 사용해 어퍼와 풋베드에 "
                "편안하고 유연한 착용감을 더했습니다."
            ),
            "order": 1,
            "careguide": footwear_careguide,
        },
    )

    eva_platform, _ = Material.objects.update_or_create(
        name="EVA Platform Sole",
        defaults={
            "description": (
                "가벼운 EVA 플랫폼 솔을 적용해 "
                "안정적인 쿠셔닝과 편안한 착화감을 제공합니다."
            ),
            "order": 2,
            "careguide": footwear_careguide,
        },
    )

    visetos_print, _ = Material.objects.update_or_create(
        name="Visetos Monogram Print",
        defaults={
            "description": (
                "램스킨 어퍼에 MCM의 시그니처 "
                "비세토스 모노그램을 프린트했습니다."
            ),
            "order": 3,
            "careguide": footwear_careguide,
        },
    )

    gold_tone_hardware = get_common_material(
        "Gold-Tone Metal Hardware",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            lambskin_leather,
            eva_platform,
            visetos_print,
            gold_tone_hardware,
        ],
    )
    
    return product


def seed_product_13():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="모노그램 플록 포켓 웨스턴 셔츠",
        defaults={
            "category": Product.Category.TOP,
            "specs": {
                "fit": "Regular Fit",
                "closure": "Button Closure",
                "sleeve": "Long Sleeve",
                "pocket": "Chest Pocket · Visetos Monogram Flock Print",
            },
            "background": {
                "description": (
                    "레이온과 폴리에스터 혼방 소재로 제작된 롱 슬리브 셔츠에 "
                    "웨스턴 스타일의 디테일을 더했습니다. "
                    "바이에른 다이아몬드 실루엣에서 영감을 받은 "
                    "기하학적인 숄더 패널과 비세토스 모노그램 포켓으로 "
                    "MCM의 헤리티지를 은은하게 표현했습니다."
                ),
                "design_details": {
                    "SHOULDER": "Western-Style Shoulder Panel",
                    "MOTIF": "Bavarian Diamond-Inspired Geometric Detail",
                    "POCKET": "Visetos Monogram Flock Print Pocket",
                    "COLOR": "Della Robbia Blue",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = ["40IT", "42IT", "44IT"]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Della Robbia Blue",
            defaults={
                # 원문 상단 가격 690,000원 기준
                "price": 690000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    rayon_polyester, _ = Material.objects.update_or_create(
        name="Rayon-Polyester Blend",
        defaults={
            "description": (
                "레이온 35%와 폴리에스터 65%를 혼방한 소재로 제작해 "
                "셔츠 특유의 자연스러운 실루엣을 완성했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "손세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 피해주세요.",
                "04": "다림질할 때는 천을 대고 다림질해 주세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.get_or_create(
        material=rayon_polyester,
        product=product,
    )

    return product


def seed_product_14():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="부클레 팬츠",
        defaults={
            "category": Product.Category.BOTTOM,
            "specs": {
                "fit": "Regular Fit",
                "silhouette": "Wide Leg",
                "closure": "Button & Zip Closure",
                "pocket": "Front Side Pockets · Back Welt Pocket",
            },
            "background": {
                "description": (
                    "네이비 컬러의 와이드 레그 부클레 팬츠에 "
                    "화이트 배색 디테일을 더해 세련된 대비를 완성했습니다. "
                    "로고 각인 골드 톤 메탈 버튼이 클래식한 분위기를 더하며, "
                    "매칭 재킷과 함께 셋업으로 연출할 수 있습니다."
                ),
                "design_details": {
                    "SILHOUETTE": "Wide Leg Design",
                    "COLOR": "Navy · White Contrast",
                    "HARDWARE": "Logo-Engraved Gold-Tone Metal Buttons",
                    "STYLING": "Matching Jacket Styling",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = ["38IT", "40IT", "42IT", "44IT"]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Navy Blazer",
            defaults={
                "price": 790000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    boucle_fabric, _ = Material.objects.update_or_create(
        name="Bouclé Fabric",
        defaults={
            "description": (
                "49% 폴리에스터, 42% 코튼, 9% 폴리아미드를 "
                "혼방한 부클레 소재로 제작했습니다. "
                "폴리에스터 트림을 더해 소재의 디테일을 완성했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "손세탁으로 관리해 주세요. 드라이클리닝은 하지 마세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 하지 마세요.",
                "04": (
                    "다림질할 때는 천을 덮어 다려 주세요. "
                    "마찰로 인한 필링은 자연스럽게 발생할 수 있습니다."
                ),
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.get_or_create(
        material=boucle_fabric,
        product=product,
    )

    return product


def seed_product_15():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="송아지 가죽 플랫폼 로퍼",
        defaults={
            "category": Product.Category.SHOES,
            "specs": {
                "material": "100% Calfskin",
                "sole": "Vibram® EVA Platform Outsole",
                "hardware": "Gold-Tone Metal",
                "fit": "Platform Loafer · Regular Fit",
            },
            "background": {
                "description": (
                    "MCM의 장인 정신과 가죽 공예 기술을 현대적으로 재해석한 "
                    "플랫폼 로퍼입니다. "
                    "블랙 카프스킨에 바이에른 다이아몬드에서 영감을 받은 "
                    "메탈 스터드 장식을 더했습니다. "
                    "Vibram® EVA 플랫폼 솔과 부드러운 카프스킨 풋베드가 "
                    "편안한 착화감과 구조적인 실루엣을 제공합니다."
                ),
                "collection": "MCM Footwear",
                "design_details": {
                    "DESIGN": "Platform Loafer",
                    "SIGNATURE": "Bavarian Diamond Studs",
                    "HERITAGE": "MCM Leather Craftsmanship",
                },
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
        "41IT",
        "42IT",
        "43IT",
    ]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Black",
            defaults={
                "price": 930000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    footwear_careguide = {
        "01": "어퍼는 살짝 적신 부드러운 면 천으로 가볍게 닦아주세요.",
        "02": "아웃솔은 부드러운 브러시를 사용해 관리해 주세요.",
        "03": "물, 알코올, 향수, 화장품 및 오일과의 접촉을 피해 주세요.",
        "04": "제품이 젖었을 경우 실온에서 충분히 건조해 주세요.",
    }

    italian_calfskin = get_common_material(
        "Italian Calfskin Leather",
        order=1,
    )

    calfskin_footbed, _ = Material.objects.update_or_create(
        name="Calfskin Footbed",
        defaults={
            "description": (
                "부드러운 카프스킨을 풋베드에 적용해 "
                "편안한 착화감을 제공합니다."
            ),
            "order": 2,
            "careguide": footwear_careguide,
        },
    )

    vibram_platform, _ = Material.objects.update_or_create(
        name="Vibram® EVA Platform",
        defaults={
            "description": (
                "가볍고 안정적인 Vibram® EVA 플랫폼 아웃솔을 적용했습니다."
            ),
            "order": 3,
            "careguide": footwear_careguide,
        },
    )

    gold_tone_hardware = get_common_material(
        "Gold-Tone Metal Hardware",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            italian_calfskin,
            calfskin_footbed,
            vibram_platform,
            gold_tone_hardware,
        ],
    )
    
    return product


def seed_product_16():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="비세토스 샌들",
        defaults={
            "category": Product.Category.SHOES,
            "specs": {
                "material": "Visetos Monogram Canvas · Calf Leather",
                "sole": "EVA Outsole",
                "hardware": "Silver-Tone Diamond Metal Buckle",
                "fit": "Adjustable Strap · Regular Fit",
            },
            "background": {
                "description": (
                    "시그니처 비세토스 모노그램 캔버스에 "
                    "바이에른 다이아몬드에서 영감을 받은 메탈 버클을 더한 샌들입니다. "
                    "이탈리아산 카프 레더 트림과 로고 풋베드가 "
                    "클래식한 MCM 헤리티지와 편안한 착화감을 함께 완성합니다."
                ),
                "collection": "Visetos Collection",
                "design_details": {
                    "DESIGN": "Adjustable Strap Sandal",
                    "SIGNATURE": "Bavarian Diamond Buckle",
                    "HERITAGE": "MCM Leather Craftsmanship",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = ["Black", "Cognac"]

    sizes = [
        "36IT",
        "37IT",
        "38IT",
        "39IT",
        "41IT",
        "42IT",
        "43IT",
    ]

    for color in colors:
        for size in sizes:
            ProductDetail.objects.update_or_create(
                product=product,
                size=size,
                color=color,
                defaults={
                    "price": 770000,
                },
            )

    # =========================
    # 3. Material
    # =========================

    sandal_careguide = {
        "01": "직사광선과 열, 비를 피해 건조한 곳에 보관해 주세요.",
        "02": "아웃솔은 부드러운 브러시를 사용해 관리해 주세요.",
        "03": "갑피는 살짝 적신 부드러운 면 천으로 닦아주세요.",
        "04": "제품이 젖거나 습기에 장시간 노출되지 않도록 주의해 주세요.",
    }

    # 기존 공통 소재와 동일 정보 유지
    visetos = get_common_material(
        "Visetos Monogram Canvas",
        order=1,
    )

    italian_calf_leather, _ = Material.objects.update_or_create(
        name="Italian Calf Leather",
        defaults={
            "description": (
                "이탈리아산 카프 레더를 트림과 풋베드, "
                "안감에 적용했습니다."
            ),
            "order": 2,
            "careguide": sandal_careguide,
        },
    )

    eva_outsole, _ = Material.objects.update_or_create(
        name="EVA Outsole",
        defaults={
            "description": (
                "가볍고 편안한 착화감을 제공하는 EVA 아웃솔을 사용했습니다."
            ),
            "order": 3,
            "careguide": sandal_careguide,
        },
    )

    silver_buckle, _ = Material.objects.update_or_create(
        name="Silver-Tone Metal Buckle",
        defaults={
            "description": (
                "바이에른 다이아몬드에서 영감을 받은 "
                "실버톤 메탈 버클 하드웨어를 적용했습니다."
            ),
            "order": 4,
            "careguide": sandal_careguide,
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos,
            italian_calf_leather,
            eva_outsole,
            silver_buckle,
        ],
    )
    
    return product

def seed_product_17():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="양가죽 쇼츠",
        defaults={
            "category": Product.Category.BOTTOM,
            "specs": {
                "fit": "Regular Fit",
                "material": "100% Lambskin Leather",
                "pocket": "Back Welt Pocket",
                "trim": "Faux Leather Trim",
            },
            "background": {
                "description": (
                    "최상급 램스킨 가죽으로 완성한 쇼츠에 "
                    "뮌헨 바이에른 다이아몬드에서 영감을 받은 "
                    "로고 패치를 더했습니다. "
                    "화이트 배색 사이드 트리밍과 로고 모티프가 "
                    "가죽의 정제된 실루엣에 선명한 대비를 더합니다."
                ),
                "design_details": {
                    "LOGO PATCH": "Diamond Logo Leather Patch",
                    "SIDE DETAIL": "White Contrast Logo Trim",
                    "POCKET": "Back Welt Pocket",
                    "SILHOUETTE": "Regular Fit",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    ProductDetail.objects.update_or_create(
        product=product,
        size="40IT",
        color="Black",
        defaults={
            "price": 990000,
        },
    )

    # =========================
    # 3. Material
    # =========================

    lambskin, _ = Material.objects.update_or_create(
        name="100% Lambskin Leather",
        defaults={
            "description": (
                "부드러운 최상급 램스킨 100%를 바디에 사용해 "
                "정제된 가죽 실루엣을 완성했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "드라이클리닝만 가능합니다.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 피해주세요.",
                "04": "거친 표면과의 마찰을 피해주세요.",
            },
        },
    )

    faux_leather, _ = Material.objects.update_or_create(
        name="Faux Leather",
        defaults={
            "description": (
                "인조 가죽 트림을 사용해 "
                "화이트 배색 디테일을 완성했습니다."
            ),
            "order": 2,
            "careguide": {
                "01": "거친 표면과의 마찰을 피해주세요.",
                "02": "표면에 강한 세정제를 사용하지 마세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    for material in [
        lambskin,
        faux_leather,
    ]:
        MaterialProduct.objects.get_or_create(
            material=material,
            product=product,
        )

    return product

def seed_product_18():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="루렉스 데님 모노그램 포켓 셔츠",
        defaults={
            "category": Product.Category.TOP,
            "specs": {
                "fit": "Oversized Fit",
                "closure": "Metal Logo Button Closure",
                "sleeve": "Long Sleeve",
                "collar": "Stud-Detail Collar",
            },
            "background": {
                "description": (
                    "은은한 광택이 감도는 인디고 데님에 "
                    "오버사이즈 실루엣을 적용한 유니섹스 셔츠입니다. "
                    "가슴 포켓에는 시그니처 비세토스 모노그램 자수를 더하고, "
                    "로고 각인 메탈 버튼과 다이아몬드 스터드 디테일을 적용해 "
                    "MCM의 헤리티지를 표현했습니다."
                ),
                "design_details": {
                    "POCKET": "Visetos Monogram Embroidery",
                    "CLOSURE": "Metal Logo Button",
                    "COLLAR": "Diamond Stud Detail",
                    "SILHOUETTE": "Oversized Unisex Fit",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = ["46IT", "48IT", "50IT"]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Indigo",
            defaults={
                "price": 830000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    # 11번과 동일한 Material이므로 내용/order도 동일
    metallic_lurex_denim = get_common_material(
        "Metallic Lurex Denim",
        order=1,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [metallic_lurex_denim],
    )
    
    return product

def seed_product_19():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="New Liz 엠보스드 모노그램 레더 쇼퍼",
        defaults={
            "category": Product.Category.BAG,
            "specs": {
                "dimensions": {
                    "S": "약 17 x 25 x 31 cm",
                    "M": "약 17 x 30 x 35 cm",
                },
                "closure": "Hook Closure",
                "strap": {
                    "S": "Leather Handle Strap · 26 cm",
                    "M": "Leather Handle Strap · 26.5 cm",
                },
                "storage": {
                    "S": "Tablet · Mobile Phone · AirPods · AirPods Max",
                    "M": "Laptop · Tablet · AirPods Max · Tumbler",
                },
            },
            "background": {
                "description": (
                    "풀그레인 가죽에 MCM의 시그니처 비세토스 모노그램을 "
                    "엠보싱으로 표현한 Liz 쇼퍼백입니다. "
                    "넉넉한 가죽 핸들 스트랩과 로고 브라스 플레이트를 더해 "
                    "실용성과 MCM의 헤리티지를 함께 담았습니다. "
                    "내부에는 탈착 가능한 레더 파우치가 포함되어 "
                    "단독 클러치로도 활용할 수 있습니다."
                ),
                "collection": "Liz Collection",
                "design_details": {
                    "DESIGN": "Embossed Visetos",
                    "SIGNATURE": "Detachable Leather Pouch",
                    "HERITAGE": "MCM Monogram",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    prices = {
        "S": 1350000,
        "M": 1490000,
    }

    for size, price in prices.items():
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Black",
            defaults={
                "price": price,
            },
        )

    # =========================
    # 3. Material
    # =========================

    bag_careguide = {
        "01": (
            "더스트 백에 넣어 직사광선과 밝은 빛을 피해 "
            "서늘하고 건조한 곳에 보관해 주세요."
        ),
        "02": (
            "표면이 젖거나 오염되었을 경우 "
            "밝은색의 흡수성 천으로 닦아주세요."
        ),
        "03": "가죽이 젖거나 얼룩지지 않도록 주의해 주세요.",
        "04": "비누나 솔벤트를 사용하지 말고 거친 표면과의 마찰을 피해주세요.",
    }

    full_grain_leather, _ = Material.objects.update_or_create(
        name="Full-Grain Leather",
        defaults={
            "description": (
                "풀그레인 가죽을 바디에 사용했습니다. "
                "가죽 핸들 스트랩과 탈착 가능한 레더 파우치에도 "
                "가죽 소재를 적용했습니다."
            ),
            "order": 1,
            "careguide": bag_careguide,
        },
    )

    cobalt_brass = get_common_material(
        "Cobalt Brass Hardware",
        order=3,
    )

    suede_microfiber = get_common_material(
        "Suede-Finish Microfiber",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            full_grain_leather,
            cobalt_brass,
            suede_microfiber,
        ],
    )
    
    return product


def seed_product_20():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="Toni 비세토스 상단 지퍼 쇼퍼",
        defaults={
            "category": Product.Category.BAG,
            "specs": {
                "dimensions": {
                    "Extra Mini": "약 9 x 16 x 14 cm",
                    "Mini": "약 10 x 19 x 19 cm",
                },
                "closure": "Top Zip Closure",
                "strap": {
                    "Extra Mini": "Detachable & Adjustable · 100–126 cm",
                    "Mini": "Detachable & Adjustable · 108–132 cm",
                },
                "storage": {
                    "Extra Mini": (
                        "Mobile Phone · AirPods · Card Wallet · Lipstick"
                    ),
                    "Mini": (
                        "Mobile Phone · AirPods · Card Wallet · Lipstick · "
                        "Sunglasses · Hand Cream"
                    ),
                },
            },
            "background": {
                "description": (
                    "비세토스 캔버스와 가죽으로 완성된 Toni 쇼퍼는 "
                    "기하학적인 디자인으로 시각적인 개성과 실용성을 보여줍니다. "
                    "상단 지퍼 클로저와 가죽 탑 핸들이 안정적인 수납과 "
                    "편안한 휴대성을 제공하며, 탈부착 및 길이 조절이 가능한 "
                    "가죽 스트랩과 D링 디테일을 통해 "
                    "MCM의 클래식한 디자인 코드를 현대적으로 담아냈습니다."
                ),
                "collection": "Visetos Collection",
                "design_details": {
                    "DESIGN": "Geometric Structure",
                    "SIGNATURE": "Leather Top Handle",
                    "HERITAGE": "MCM Luggage",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = [
        "Cognac",
        "Black",
        "Beige + Black",
        "Khaki Moss",
        "Soft Pink",
        "Cinnamon",
        "White",
    ]

    prices = {
        "Extra Mini": 850000,
        "Mini": 970000,
    }

    for color in colors:
        for size, price in prices.items():
            ProductDetail.objects.update_or_create(
                product=product,
                size=size,
                color=color,
                defaults={
                    "price": price,
                },
            )

    # =========================
    # 3. Material
    # =========================

    visetos = get_common_material(
        "Visetos Monogram Canvas",
        order=1,
    )

    nappa_leather = get_common_material(
        "Nappa Leather",
        order=2,
    )

    cobalt_brass = get_common_material(
        "Cobalt Brass Hardware",
        order=3,
    )

    suede_microfiber = get_common_material(
        "Suede-Finish Microfiber",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos,
            nappa_leather,
            cobalt_brass,
            suede_microfiber,
        ],
    )
    
    return product

def seed_product_21():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="Pina 비세토스 스터드 장식 토트",
        defaults={
            "category": Product.Category.BAG,
            "specs": {
                "dimensions": {
                    "M": "약 13 x 30 x 24 cm",
                    "L": "약 18 x 41 x 32 cm",
                },
                "strap": {
                    "M": "107.5–131.5 cm · Handle Drop 11 cm",
                    "L": "112.5–136.5 cm · Handle Drop 12 cm",
                },
                "closure": "Two-Way Zip Closure",
                "pocket": "Internal Slip Pocket · Zipper Compartment",
                "storage": {
                    "M": "Tablet · Headphones · Pouch · Wallet · Bottle",
                    "L": "Laptop · Tablet · Headphones · Pouch · Wallet · Bottle · Note",
                },
            },
            "background": {
                "description": (
                    "비세토스 모노그램 캔버스와 나파 가죽을 조합한 "
                    "보울러 실루엣의 토트백으로 클래식한 MCM 헤리티지를 담았습니다. "
                    "바이에른 다이아몬드와 라우렐 엠블럼에서 영감을 받은 "
                    "메탈 스터드 장식으로 시그니처 디자인을 강조했습니다."
                ),
                "collection": "Visetos Collection",
                "design_details": {
                    "DESIGN": "Bowler Silhouette",
                    "SIGNATURE": "Metal Stud Details",
                    "HERITAGE": "Bavarian Diamond & Laurel",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    prices = {
        "M": 1690000,
        "L": 1850000,
    }

    for size, price in prices.items():
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Cognac",
            defaults={
                "price": price,
            },
        )

    # =========================
    # 3. Material
    # =========================

    visetos = get_common_material(
        "Visetos Monogram Canvas",
        order=1,
    )

    nappa_leather = get_common_material(
        "Nappa Leather",
        order=2,
    )

    gold_plated_brass = get_common_material(
        "24K Gold-Plated Brass",
        order=3,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos,
            nappa_leather,
            gold_plated_brass,
        ],
    )
    
    return product


def seed_product_22():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="MCM 비세토스 파크베어 참",
        defaults={
            "category": Product.Category.ACCESSORY,
            "specs": {
                "dimensions": "약 8 x 6 x 8 cm",
                "body": "Visetos Monogram Canvas",
                "trim": "Natural Leather",
                "hardware": "24K Gold-Plated Metal",
            },
            "background": {
                "description": (
                    "뮌헨 하우스를 대표하는 아이코닉한 베어 참으로, "
                    "비세토스 모노그램 캔버스와 천연 가죽 트림을 조합해 "
                    "위트 있는 포인트를 완성했습니다. "
                    "24K 골드 도금 메탈 키링과 로고가 각인된 스프링 클래스프를 더해 "
                    "MCM 특유의 헤리티지를 표현했습니다."
                ),
                "collection": "MCM Accessories",
                "design_details": {
                    "DESIGN": "Bear Charm",
                    "SIGNATURE": "Visetos Monogram",
                    "HERITAGE": "MCM Bear",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    ProductDetail.objects.update_or_create(
        product=product,
        size="Free",
        color="Cognac",
        defaults={
            "price": 390000,
        },
    )

    # =========================
    # 3. Material
    # =========================

    visetos = get_common_material(
        "Visetos Monogram Canvas",
        order=1,
    )

    natural_leather = get_common_material(
        "Natural Leather",
        order=2,
    )

    gold_plated_metal = get_common_material(
        "24K Gold-Plated Metal",
        order=3,
    )

    key_ring, _ = Material.objects.update_or_create(
        name="Metal Key Ring & Spring Clasp",
        defaults={
            "description": (
                "메탈 키링과 로고가 각인된 스프링 클래스프를 적용해 "
                "가방과 러기지에 간편하게 연결할 수 있도록 제작했습니다."
            ),
            "order": 4,
            "careguide": {
                "01": "물과 습기에 장시간 노출되지 않도록 주의해 주세요.",
                "02": "부드러운 마른 천으로 관리해 주세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos,
            natural_leather,
            gold_plated_metal,
            key_ring,
        ],
    )
    
    return product


def seed_product_23():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="디스코 시퀸 티셔츠",
        defaults={
            "category": Product.Category.TOP,
            "specs": {
                "fit": "Regular Fit",
                "design": "MCM Disco Sequin Logo",
                "trim": "Rib Knit Trim",
                "material": "100% Organic Cotton",
            },
            "background": {
                "description": (
                    "70년대 음악과 문화를 기념하는 시즌 테마 MCM Disco를 "
                    "티셔츠에 담아냈습니다. "
                    "반짝이는 시퀸 장식과 감각적인 타이포그래피를 조합해 "
                    "그래픽에 화려한 포인트를 더했으며, "
                    "심플한 실루엣으로 데일리하게 연출할 수 있도록 완성했습니다."
                ),
                "design_details": {
                    "GRAPHIC": "MCM Disco Logo",
                    "DETAIL": "Sequin Embroidery",
                    "THEME": "1970s Music & Culture",
                    "FIT": "Regular Fit",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    for size in ["S", "M", "L"]:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="White",
            defaults={
                "price": 450000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    organic_cotton_jersey = get_common_material(
        "Organic Cotton Jersey",
        order=1,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [organic_cotton_jersey],
    )
    
    return product


def seed_product_24():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="Stark 맥시 모노그램 레더 백팩",
        defaults={
            "category": Product.Category.BAG,
            "specs": {
                "dimensions": {
                    "S": "약 14 x 28 x 35 cm",
                    "M": "약 15 x 33 x 42 cm",
                },
                "strap": {
                    "S": "75–89 cm · Handle Drop 6 cm",
                    "M": "75–89 cm · Handle Drop 7.5 cm",
                },
                "closure": "Two-Way Zip Closure",
                "storage": {
                    "S": "Tablet · Smartphone · Earphones · Headphones · Bottle · Pouch · Wallet · Passport",
                    "M": "13-inch Laptop · Tablet · Smartphone · Earphones · Headphones · Charger · Adapter · Bottle · Pouch · Wallet · Passport",
                },
            },
            "background": {
                "description": (
                    "클래식한 Stark 백팩 실루엣에 맥시 비세토스 모노그램을 더해 "
                    "MCM의 아이코닉한 디자인을 현대적으로 재해석했습니다. "
                    "가죽 탑 핸들과 우븐 패브릭 숄더 스트랩을 조합하고 "
                    "다양한 외부 및 내부 포켓을 구성해 실용적인 수납 구조를 완성했습니다."
                ),
                "collection": "Stark Collection",
                "design_details": {
                    "DESIGN": "Maxi Monogram",
                    "SIGNATURE": "Visetos Monogram",
                    "HERITAGE": "MCM Mobility",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    # 원문 사이즈별 표 기준:
    # S = 2,390,000원 / M = 2,090,000원
    prices = {
        "S": 2390000,
        "M": 2090000,
    }

    for size, price in prices.items():
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Black",
            defaults={
                "price": price,
            },
        )

    # =========================
    # 3. Material
    # =========================

    natural_full_grain, _ = Material.objects.update_or_create(
        name="Natural Full-Grain Leather",
        defaults={
            "description": (
                "천연 풀그레인 레더를 사용해 "
                "자연스러운 가죽 질감과 견고한 소재감을 살렸습니다."
            ),
            "order": 1,
            "careguide": leather_careguide,
        },
    )

    natural_nappa = get_common_material(
        "Natural Nappa Leather",
        order=2,
    )

    dark_metal, _ = Material.objects.update_or_create(
        name="Dark Metal Hardware",
        defaults={
            "description": (
                "다크 메탈 하드웨어를 적용해 "
                "모노크롬 디자인과 조화를 이루는 금속 디테일을 완성했습니다."
            ),
            "order": 3,
            "careguide": {
                "01": "습기와 물에 장시간 노출되지 않도록 주의해 주세요.",
                "02": "부드러운 마른 천으로 관리해 주세요.",
            },
        },
    )

    suede_microfiber = get_common_material(
        "Suede-Finish Microfiber",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            natural_full_grain,
            natural_nappa,
            dark_metal,
            suede_microfiber,
        ],
    )
    
    return product

def seed_product_25():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="Aren 비세토스 크로스바디",
        defaults={
            "category": Product.Category.BAG,
            "specs": {
                "dimensions": {
                    "Extra Mini": "약 5 x 17 x 13 cm",
                    "S": "약 5 x 22 x 16 cm",
                },
                "strap": {
                    "Extra Mini": "79–138 cm",
                    "S": "80–140 cm",
                },
                "closure": {
                    "Extra Mini": "Main Zip Closure",
                    "S": "Main Zip Closure · Rear Magnetic Snap Closure",
                },
                "pocket": {
                    "Extra Mini": "Front Zip Pocket · Internal Open Pocket",
                    "S": "Rear External Pocket · Front Zip Pocket · 2 Internal Open Pockets",
                },
            },
            "background": {
                "description": (
                    "시그니처 비세토스 모노그램과 나파 가죽 트림이 조화를 이루는 "
                    "Aren 크로스바디는 가벼운 구조와 실용적인 수납을 갖춘 "
                    "핸즈프리 스타일입니다. "
                    "MCM의 글로벌 노마드 정신에서 영감을 받아 "
                    "일상과 여행에서 자유로운 움직임을 제공하도록 디자인했습니다."
                ),
                "collection": "Aren Collection",
                "design_details": {
                    "DESIGN": "Hands-Free & Mobility",
                    "SIGNATURE": "Visetos Monogram & Logo Plate",
                    "HERITAGE": "MCM Global Nomad",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    prices = {
        "Extra Mini": 1050000,
        "S": 1190000,
    }

    for size, price in prices.items():
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Cognac",
            defaults={
                "price": price,
            },
        )

    # =========================
    # 3. Material
    # =========================

    visetos_coated, _ = Material.objects.update_or_create(
        name="Visetos Monogram Coated Canvas",
        defaults={
            "description": (
                "MCM의 시그니처 비세토스 모노그램 코티드 캔버스를 사용해 "
                "클래식한 패턴과 견고한 내구성을 완성했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "직사광선과 밝은 빛을 피해 서늘하고 건조한 곳에 보관해 주세요.",
                "02": "표면 오염 시 부드러운 천으로 가볍게 닦아주세요.",
                "03": "비누나 솔벤트를 사용하지 마세요.",
            },
        },
    )

    nappa_leather = get_common_material(
        "Nappa Leather",
        order=2,
    )

    gold_plated_metal = get_common_material(
        "24K Gold-Plated Metal",
        order=3,
    )

    cotton_twill, _ = Material.objects.update_or_create(
        name="Cotton Twill",
        defaults={
            "description": (
                "가방 내부에 코튼 트윌 라이닝을 적용해 "
                "깔끔하고 실용적인 내부 공간을 완성했습니다."
            ),
            "order": 4,
            "careguide": {
                "01": "오염 시 부드러운 마른 천으로 관리해 주세요.",
                "02": "습기에 장시간 노출되지 않도록 주의해 주세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos_coated,
            nappa_leather,
            gold_plated_metal,
            cotton_twill,
        ],
    )
    
    return product


def seed_product_26():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="재생 나일론 및 모노그램 프린트 가죽 소재의 Aren 쇼퍼",
        defaults={
            "category": Product.Category.BAG,
            "specs": {
                "dimensions": "약 9 x 16 x 14 cm",
                "strap": "94.5–118.5 cm · Handle Drop 7.5 cm",
                "closure": "Zip Closure",
                "pocket": "Internal Pocket · Card Slot",
            },
            "background": {
                "description": (
                    "재생 나일론과 비세토스 모노그램 가죽 트림을 조합한 "
                    "엑스트라 미니 Aren 쇼퍼입니다. "
                    "컴팩트한 실루엣에 가죽 손잡이와 조절 가능한 스트랩을 더했으며, "
                    "바이에른 다이아몬드에서 영감을 받은 로고 참과 "
                    "라우렐 로고 메탈 장식으로 MCM의 헤리티지를 표현했습니다."
                ),
                "collection": "Aren Collection",
                "design_details": {
                    "DESIGN": "Mini Shopper & Hands-Free",
                    "SIGNATURE": "Visetos Monogram Leather Charm",
                    "HERITAGE": "Bavarian Diamond & Laurel",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    ProductDetail.objects.update_or_create(
        product=product,
        size="Extra Mini",
        color="Black",
        defaults={
            "price": 750000,
        },
    )

    # =========================
    # 3. Material
    # =========================

    recycled_nylon, _ = Material.objects.update_or_create(
        name="Recycled Nylon",
        defaults={
            "description": (
                "이탈리아산 재생 나일론 ECONYL®을 바디에 사용해 "
                "가볍고 실용적인 구조를 완성했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "직사광선과 밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요.",
                "02": "표면 오염 시 부드러운 천으로 가볍게 닦아주세요.",
            },
        },
    )

    visetos_leather, _ = Material.objects.update_or_create(
        name="Visetos Monogram Leather",
        defaults={
            "description": (
                "비세토스 모노그램 프린트 가죽을 트림과 스트랩에 적용해 "
                "MCM의 시그니처 패턴을 강조했습니다."
            ),
            "order": 2,
            "careguide": leather_careguide,
        },
    )

    cobalt_metal, _ = Material.objects.update_or_create(
        name="Cobalt Metal Hardware",
        defaults={
            "description": (
                "실버톤 코발트 금속 장식을 사용해 "
                "라우렐 로고와 하드웨어에 세련된 포인트를 더했습니다."
            ),
            "order": 3,
            "careguide": {
                "01": "물과 습기에 장시간 노출되지 않도록 주의해 주세요.",
                "02": "부드러운 마른 천으로 관리해 주세요.",
            },
        },
    )

    fabric_lining = get_common_material(
        "Fabric Lining",
        order=4,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            recycled_nylon,
            visetos_leather,
            cobalt_metal,
            fabric_lining,
        ],
    )
    
    return product

def seed_product_27():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="울 트윌 모노그램 팬츠",
        defaults={
            "category": Product.Category.BOTTOM,
            "specs": {
                "product_type": "Oversized Pants",
                "closure": "Hidden Zip Closure",
                "pocket": "Front Side Pockets · Back Welt Pocket",
                "waistband": "Visetos Monogram Jacquard Elastic Waistband",
            },
            "background": {
                "description": (
                    "동물 복지를 고려해 생산된 울 소재에 "
                    "오버사이즈 실루엣을 적용한 팬츠입니다. "
                    "허리에는 비세토스 모노그램 자카드 밴드를 더하고, "
                    "앞면 사이드 포켓에는 정교한 스티치 패턴을 적용했습니다."
                ),
                "design_details": {
                    "WAISTBAND": "Visetos Monogram Jacquard Elastic",
                    "POCKET DETAIL": "Stitch Pattern",
                    "CLOSURE": "Hidden Zip Closure",
                    "SILHOUETTE": "Oversized Fit",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    for size in ["38IT", "40IT", "42IT", "44IT"]:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Light Brown",
            defaults={
                "price": 970000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    japanese_wool, _ = Material.objects.update_or_create(
        name="Japanese Wool",
        defaults={
            "description": (
                "동물 복지를 고려해 뮬징을 하지 않은 "
                "일본산 울 100%를 사용했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "드라이클리닝만 가능합니다.",
                "02": "물세탁하지 마세요.",
                "03": "표백제를 사용하지 마세요.",
                "04": "기계 건조하지 마세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.get_or_create(
        material=japanese_wool,
        product=product,
    )

    return product


def seed_product_28():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="모노그램 레더 네오 터레인 로 스니커즈",
        defaults={
            "category": Product.Category.SHOES,
            "specs": {
                "material": "100% Calf Leather",
                "insole": "OrthoLite® Memory Foam",
                "outsole": "Rubber Outsole",
                "fit": "Low-Top Sneakers · Regular Fit",
            },
            "background": {
                "description": (
                    "클래식 비세토스 모노그램을 엠보싱 처리한 "
                    "이탈리안 카프스킨 어퍼로 완성한 로우탑 스니커즈입니다. "
                    "바이에른 다이아몬드에서 영감을 받은 텅 라벨과 "
                    "가죽 힐 패치를 더했으며, 메시를 덧댄 가죽 안감과 "
                    "OrthoLite® 인솔로 편안한 착화감을 제공합니다."
                ),
                "collection": "MCM Footwear",
                "design_details": {
                    "DESIGN": "Low-Top Sneaker",
                    "SIGNATURE": "Embossed Visetos Monogram",
                    "HERITAGE": "Bavarian Diamond",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    for size in ["40IT", "41IT", "42IT", "43IT"]:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Black",
            defaults={
                "price": 770000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    sneaker_careguide = {
        "01": "아웃솔은 부드러운 브러시로, 갑피는 살짝 적신 면 천으로 닦아주세요.",
        "02": "클리닝 후 실내 온도에서 충분히 건조해 주세요.",
        "03": "물, 향수, 화장품, 오일 등의 접촉을 피해 주세요.",
        "04": "직사광선과 밝은 조명을 피해 서늘하고 건조한 곳에 보관해 주세요.",
    }

    italian_calfskin = get_common_material(
        "Italian Calfskin Leather",
        order=1,
    )

    embossed_visetos, _ = Material.objects.update_or_create(
        name="Embossed Visetos Monogram",
        defaults={
            "description": (
                "시그니처 비세토스 모노그램을 엠보싱 처리해 "
                "입체적인 질감과 MCM의 아이덴티티를 더했습니다."
            ),
            "order": 2,
            "careguide": sneaker_careguide,
        },
    )

    ortholite = get_common_material(
        "OrthoLite® Memory Foam",
        order=3,
    )
    
    rubber_outsole = get_common_material(
        "Rubber Outsole",
        order=4,
    )

    mesh_lined_leather, _ = Material.objects.update_or_create(
        name="Mesh-Lined Leather",
        defaults={
            "description": (
                "메시를 덧댄 가죽 안감을 사용해 "
                "부드러운 착용감과 통기성을 제공합니다."
            ),
            "order": 5,
            "careguide": sneaker_careguide,
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            italian_calfskin,
            embossed_visetos,
            ortholite,
            rubber_outsole,
            mesh_lined_leather,
        ],
    )
    
    return product

def seed_product_29():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="루렉스 데님 오버올 스커트",
        defaults={
            "category": Product.Category.BOTTOM,
            "specs": {
                "product_type": "Overall Skirt",
                "pocket": "Front & Back Pockets",
                "hardware": "Logo-Engraved Metal Buttons · Diamond Studs",
                "logo_detail": "Silicone MCM Logo Plate · Visetos Monogram Patch",
            },
            "background": {
                "description": (
                    "70년대 스타일을 현대적으로 재해석한 오버롤 스커트에 "
                    "메탈릭 루렉스 섬유와 MCM의 시그니처 디테일을 더했습니다. "
                    "가슴 포켓의 실리콘 MCM 로고 플레이트와 "
                    "뒷면의 비세토스 모노그램 패치가 브랜드의 헤리티지를 표현합니다."
                ),
                "design_details": {
                    "LOGO PLATE": "Silicone MCM Logo Plate",
                    "BACK DETAIL": "Visetos Monogram Patch",
                    "POCKET": "Front & Back Pockets",
                    "HARDWARE": "Logo-Engraved Metal Buttons · Diamond Studs",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    for size in ["XS", "S", "M"]:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Indigo",
            defaults={
                "price": 890000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    metallic_lurex_denim = get_common_material(
        "Metallic Lurex Denim",
        order=1,
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [metallic_lurex_denim],
    )
    
    return product

def seed_product_30():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="Diamante 퀼팅 레더 로우탑 스니커즈",
        defaults={
            "category": Product.Category.SHOES,
            "specs": {
                "material": "Quilted Leather · Natural Leather",
                "sole": "Diamanté Rubber Sole",
                "lining": "Mesh Lining",
                "fit": "Low-Top Sneakers · Regular Fit",
            },
            "background": {
                "description": (
                    "전통적인 러닝화를 현대적으로 재해석한 로우탑 스니커즈입니다. "
                    "퀼팅 레더 어퍼에 시그니처 비세토스 모노그램을 더하고, "
                    "뮌헨의 바이에른 다이아몬드에서 영감을 받은 3D 패턴으로 "
                    "MCM만의 아이코닉한 디자인을 완성했습니다. "
                    "디아망떼 러버 아웃솔과 듀얼 밀도 미드솔을 적용해 "
                    "편안한 착화감과 세련된 실루엣을 제공합니다."
                ),
                "collection": "MCM Footwear",
                "design_details": {
                    "DESIGN": "Quilted Low-Top Sneaker",
                    "SIGNATURE": "Visetos Monogram Print",
                    "HERITAGE": "Bavarian Diamond",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = ["Black", "Cognac"]
    sizes = ["40IT", "41IT", "42IT", "43IT"]

    for color in colors:
        for size in sizes:
            ProductDetail.objects.update_or_create(
                product=product,
                size=size,
                color=color,
                defaults={
                    "price": 630000,
                },
            )

    # =========================
    # 3. Material
    # =========================

    sneaker_careguide = {
        "01": "아웃솔은 부드러운 브러시로, 갑피는 살짝 적신 부드러운 면 천으로 닦아주세요.",
        "02": "제품이 젖었을 경우 인솔을 분리한 후 실온에서 완전히 건조해 주세요.",
        "03": "물, 향수, 화장품, 오일 등 알코올 성분과의 접촉을 피해 주세요.",
        "04": "직사광선과 열, 비를 피해 건조한 곳에 보관해 주세요.",
    }

    quilted_leather, _ = Material.objects.update_or_create(
        name="Quilted Leather",
        defaults={
            "description": (
                "비세토스 모노그램 프린트가 더해진 "
                "퀼팅 레더를 어퍼에 사용했습니다."
            ),
            "order": 1,
            "careguide": sneaker_careguide,
        },
    )

    natural_leather = get_common_material(
        "Natural Leather",
        order=2,
    )

    mesh_lining, _ = Material.objects.update_or_create(
        name="Mesh Lining",
        defaults={
            "description": (
                "메시 라이닝을 사용해 "
                "부드럽고 쾌적한 착용감을 제공합니다."
            ),
            "order": 3,
            "careguide": sneaker_careguide,
        },
    )

    diamante_rubber, _ = Material.objects.update_or_create(
        name="Diamanté Rubber Sole",
        defaults={
            "description": (
                "디아망떼 러버 아웃솔과 듀얼 밀도 미드솔을 적용해 "
                "안정적인 착화감과 쿠셔닝을 제공합니다."
            ),
            "order": 4,
            "careguide": sneaker_careguide,
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            quilted_leather,
            natural_leather,
            mesh_lining,
            diamante_rubber,
        ],
    )
    
    return product

def seed_product_31():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="울 리사이클 캐시미어 라우렐 크롭 카디건",
        defaults={
            "category": Product.Category.TOP,
            "specs": {
                "fit": "Cropped Fit",
                "neckline": "V-Neck",
                "closure": "Button Closure",
                "detail": "Laurel Logo Embroidery · MCM Sleeve Embroidery",
                "size_measurements": {
                    "XS": {
                        "한국 사이즈": 44,
                        "신장": "160–165 cm",
                        "가슴둘레": "84–86 cm",
                    },
                    "S": {
                        "한국 사이즈": 55,
                        "신장": "165–170 cm",
                        "가슴둘레": "88–90 cm",
                    },
                    "M": {
                        "한국 사이즈": 66,
                        "신장": "167–172 cm",
                        "가슴둘레": "92–96 cm",
                    },
                    "L": {
                        "한국 사이즈": 77,
                        "신장": "168–173 cm",
                        "가슴둘레": "98–102 cm",
                    },
                },
            },
            "background": {
                "description": (
                    "슈퍼파인 울과 재활용 캐시미어로 짜인 "
                    "크롭 V넥 카디건입니다. "
                    "라우렐 로고 자수로 MCM의 클래식한 아이덴티티를 표현하고, "
                    "오른쪽 소매에는 MCM 이니셜 자수를 더해 "
                    "절제된 포인트를 완성했습니다."
                ),
                "design_details": {
                    "NECKLINE": "V-Neck",
                    "LOGO": "Laurel Logo Embroidery",
                    "SLEEVE DETAIL": "MCM Initials Embroidery",
                    "SILHOUETTE": "Cropped Cardigan",
                },
                "material_details": {
                    "BODY": "70% Wool",
                    "CASHMERE": "30% Recycled Cashmere",
                    "KNIT": "Wool & Cashmere Knit",
                    "TRIM": "Rib Knit Trim",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = ["XS", "S", "M", "L"]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Blush Pink",
            defaults={
                "price": 850000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    wool_cashmere, _ = Material.objects.update_or_create(
        name="Superfine Wool & Recycled Cashmere",
        defaults={
            "description": (
                "슈퍼파인 울 70%와 재활용 캐시미어 30%를 혼방한 "
                "니트 소재로 제작했습니다. "
                "립 니트 트림을 더해 카디건의 구조감을 완성했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "손세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "건조기 사용을 피해주세요.",
                "04": "서늘하고 건조한 곳에 보관해 주세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    MaterialProduct.objects.get_or_create(
        material=wool_cashmere,
        product=product,
    )

    return product


def seed_product_32():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="별자리 데님 진",
        defaults={
            "category": Product.Category.BOTTOM,
            "specs": {
                "product_type": "Oversized Denim Jeans",
                "design": "5-Pocket Design",
                "detail": "Laser-Printed Visetos Monogram",
                "patch": "Visetos Monogram Leather Patch",
                "size_measurements": {
                    "38IT": {
                        "한국 사이즈": 44,
                        "신장": "160–165 cm",
                        "허리": "24–25",
                    },
                    "40IT": {
                        "한국 사이즈": 55,
                        "신장": "165–170 cm",
                        "허리": "26–27",
                    },
                    "42IT": {
                        "한국 사이즈": 66,
                        "신장": "167–172 cm",
                        "허리": "28–29",
                    },
                    "44IT": {
                        "한국 사이즈": 77,
                        "신장": "168–173 cm",
                        "허리": "30–31",
                    },
                },
            },
            "background": {
                "description": (
                    "시즌의 별자리 콘셉트를 반영해 레터링과 라우렐, "
                    "다이아몬드 모티프를 별자리처럼 표현한 "
                    "오버사이즈 데님 진입니다. "
                    "곡선형 절개로 볼륨감 있는 실루엣을 완성하고, "
                    "뒷면에는 클래식한 비세토스 모노그램 프린트가 더해진 "
                    "코냑 컬러 가죽 패치를 적용했습니다."
                ),
                "design_details": {
                    "PRINT": "Laser-Printed Visetos Monogram",
                    "POCKET": "5-Pocket Design",
                    "BACK DETAIL": "Visetos Monogram Leather Patch",
                    "SILHOUETTE": "Oversized Fit",
                },
                "material_details": {
                    "BODY": "100% Cotton",
                    "POCKET LINING": "82% Polyester · 18% Cotton",
                    "PATCH": "Grain Leather",
                    "PRINT": "Laser-Printed Visetos Monogram",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    sizes = ["38IT", "40IT", "42IT", "44IT"]

    for size in sizes:
        ProductDetail.objects.update_or_create(
            product=product,
            size=size,
            color="Light Denim",
            defaults={
                "price": 790000,
            },
        )

    # =========================
    # 3. Material
    # =========================

    cotton_denim, _ = Material.objects.update_or_create(
        name="Cotton Denim",
        defaults={
            "description": (
                "100% 코튼 데님을 바디에 사용해 "
                "견고하면서도 자연스러운 데님 실루엣을 완성했습니다."
            ),
            "order": 1,
            "careguide": {
                "01": "손세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "기계 건조를 피해주세요.",
                "04": "제품의 형태와 디테일이 손상되지 않도록 주의해 주세요.",
            },
        },
    )

    grain_leather, _ = Material.objects.update_or_create(
        name="Grain Leather",
        defaults={
            "description": (
                "뒷면의 비세토스 모노그램 패치에 "
                "그레인 레더를 사용해 가죽 특유의 질감과 "
                "MCM의 헤리티지 디테일을 더했습니다."
            ),
            "order": 2,
            "careguide": leather_careguide,
        },
    )

    polyester_cotton_lining, _ = Material.objects.update_or_create(
        name="Polyester-Cotton Pocket Lining",
        defaults={
            "description": (
                "포켓 안감에는 폴리에스터 82%와 코튼 18%를 "
                "혼방한 소재를 사용했습니다."
            ),
            "order": 3,
            "careguide": {
                "01": "손세탁 또는 드라이클리닝으로 관리해 주세요.",
                "02": "표백제를 사용하지 마세요.",
                "03": "기계 건조를 피해주세요.",
            },
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    for material in [
        cotton_denim,
        grain_leather,
        polyester_cotton_lining,
    ]:
        MaterialProduct.objects.get_or_create(
            material=material,
            product=product,
        )

    return product


def seed_product_33():

    # =========================
    # 1. Product
    # =========================

    product, _ = Product.objects.update_or_create(
        name="비세토스 레더 믹스 네오 터레인 스니커즈",
        defaults={
            "category": Product.Category.SHOES,
            "specs": {
                "upper": "Visetos Monogram Canvas",
                "trim": "Calfskin Leather",
                "lining": "Mesh-Infused Calfskin",
                "insole": "OrthoLite® Insole",
                "outsole": "Rubber Outsole",
            },
            "background": {
                "description": (
                    "비세토스 모노그램 캔버스와 카프스킨 레더를 조합한 "
                    "클래식한 로우탑 스니커즈입니다. "
                    "선형적인 가죽 오버레이가 깔끔하고 구조적인 실루엣을 완성하며, "
                    "바이에른 다이아몬드에서 영감을 받은 가죽 힐 패치와 "
                    "라우렐 로고 텅 라벨로 MCM의 시그니처 헤리티지를 표현했습니다. "
                    "메시가 결합된 카프스킨 라이닝과 OrthoLite® 인솔을 적용해 "
                    "편안한 착화감을 제공합니다."
                ),
                "collection": "Visetos Collection",
                "design_details": {
                    "DESIGN": "Low-Top Sneaker",
                    "SIGNATURE": "Leather Diamond Patch",
                    "HERITAGE": "Bavarian Diamond & Laurel Logo",
                },
            },
        },
    )

    # =========================
    # 2. ProductDetail
    # =========================

    colors = [
        "Soft Pink",
        "Cognac",
    ]

    sizes = [
        "35IT",
        "36IT",
        "37IT",
        "38IT",
        "39IT",
        "40IT",
        "41IT",
    ]

    for color in colors:
        for size in sizes:
            ProductDetail.objects.update_or_create(
                product=product,
                size=size,
                color=color,
                defaults={
                    "price": 770000,
                },
            )

    # =========================
    # 3. Material
    # =========================

    sneaker_careguide = {
        "01": (
            "아웃솔은 부드러운 브러시로 가볍게 세척하고, "
            "어퍼는 살짝 적신 면 천으로 닦아주세요."
        ),
        "02": (
            "제품이 젖었을 경우 인솔을 분리하고 "
            "상온에서 충분히 건조해 주세요."
        ),
        "03": (
            "향수, 메이크업, 오일 등 수분 및 알코올 성분이 "
            "포함된 물질과의 접촉을 피해 주세요."
        ),
        "04": (
            "직사광선과 열을 피해 보관하고 "
            "제품이 젖거나 오염되지 않도록 주의해 주세요."
        ),
    }

    visetos = get_common_material(
        "Visetos Monogram Canvas",
        order=1,
    )

    calfskin_leather, _ = Material.objects.update_or_create(
        name="Calfskin Leather",
        defaults={
            "description": (
                "카프스킨 레더를 오버레이와 트림에 적용해 "
                "부드러운 질감과 구조적인 실루엣을 더했습니다."
            ),
            "order": 2,
            "careguide": sneaker_careguide,
        },
    )

    mesh_calfskin, _ = Material.objects.update_or_create(
        name="Mesh-Infused Calfskin",
        defaults={
            "description": (
                "메시가 결합된 카프스킨 라이닝을 사용해 "
                "부드럽고 편안한 착용감과 통기성을 제공합니다."
            ),
            "order": 3,
            "careguide": sneaker_careguide,
        },
    )

    ortholite_insole, _ = Material.objects.update_or_create(
        name="OrthoLite® Insole",
        defaults={
            "description": (
                "OrthoLite® 인솔을 적용해 "
                "발에 편안한 쿠셔닝과 일상적인 착화감을 제공합니다."
            ),
            "order": 4,
            "careguide": sneaker_careguide,
        },
    )

    # =========================
    # 4. MaterialProduct
    # =========================

    connect_materials(
        product,
        [
            visetos,
            calfskin_leather,
            mesh_calfskin,
            ortholite_insole,
        ],
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
        branch, _ = Branch.objects.update_or_create(
            name=data["name"],
            latitude=data["latitude"],
            longitude=data["longitude"],
        )

        BusinessHours.objects.update_or_create(
            branch=branch,
            open=data["open"],
            close=data["close"],
        )

        branches[data["name"]] = branch

    return branches

def seed_stocks(products, branches):

    branch_list = list(branches.values())

    for product_index, product in enumerate(products):

        details = product.details.all().order_by("id")

        for detail_index, detail in enumerate(details):

            for branch_index, branch in enumerate(branch_list):

                # 0 ~ 3개 사이의 임의 재고
                # 실행할 때마다 바뀌지 않도록 고정된 패턴 사용
                quantity = (
                    product_index
                    + detail_index
                    + branch_index
                ) % 4

                Stock.objects.update_or_create(
                    branch=branch,
                    detail=detail,
                    defaults={
                        "quantity": quantity,
                    },
                )

PRODUCT_IMAGES = {
    1: "products/1.png",
    2: "products/2.png",
    3: "products/3.png",
    4: "products/4.png",
    5: "products/5.png",
    6: "products/6.png",
    7: "products/7.png",
    8: "products/8.png",
    9: "products/9.png",
    10: "products/10.png",
    11: "products/11.png",
    12: "products/12.png",
    13: "products/13.png",
    14: "products/14.png",
    15: "products/15.png",
    16: "products/16.png",
    17: "products/17.png",
    18: "products/18.png",
    19: "products/19.png",
    20: "products/20.png",
    21: "products/21.png",
    22: "products/22.png",
    23: "products/23.png",
    24: "products/24.png",
    25: "products/25.png",
    26: "products/26.png",
    27: "products/27.png",
    28: "products/28.png",
    29: "products/29.png",
    30: "products/30.png",
    31: "products/31.png",
    32: "products/32.png",
    33: "products/33.png",
}

def seed_product_images(products):

    for product_number, product in enumerate(
        products,
        start=1,
    ):
        image_path = PRODUCT_IMAGES.get(
            product_number
        )

        if not image_path:
            continue

        # 해당 제품의 첫 번째 ProductDetail을
        # 대표 Detail로 사용
        detail = (
            product.details
            .order_by("id")
            .first()
        )

        if not detail:
            print(
                f"[WARNING] Product {product_number}: "
                "ProductDetail이 없습니다."
            )
            continue

        ProductImage.objects.update_or_create(
            detail=detail,
            order=0,
            defaults={
                "image": image_path,
            },
        )

class Command(BaseCommand):
    help = "제품, 지점, 재고 seed 데이터 생성"

    def handle(self, *args, **options):

        products = [
            seed_product_1(),
            seed_product_2(),
            seed_product_3(),
            seed_product_4(),
            seed_product_5(),
            seed_product_6(),
            seed_product_7(),
            seed_product_8(),
            seed_product_9(),
            seed_product_10(),
            seed_product_11(),
            seed_product_12(),
            seed_product_13(),
            seed_product_14(),
            seed_product_15(),
            seed_product_16(),
            seed_product_17(),
            seed_product_18(),
            seed_product_19(),
            seed_product_20(),
            seed_product_21(),
            seed_product_22(),
            seed_product_23(),
            seed_product_24(),
            seed_product_25(),
            seed_product_26(),
            seed_product_27(),
            seed_product_28(),
            seed_product_29(),
            seed_product_30(),
            seed_product_31(),
            seed_product_32(),
            seed_product_33(),
        ]

        # 제품 이미지 DB 연결
        seed_product_images(products)

        branches = seed_branches()

        seed_stocks(products, branches)

        self.stdout.write(
            self.style.SUCCESS(
                "제품 1~33 및 지점/영업시간/재고 seed 데이터 생성 완료"
            )
        )