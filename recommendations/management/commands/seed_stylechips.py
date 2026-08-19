from django.core.management.base import BaseCommand

from recommendations.models import StyleChip


STYLE_CHIPS = [
    {
        "code": "CLASSIC",
        "label": "클래식",
    },
    {
        "code": "HERITAGE",
        "label": "헤리티지",
    },
    {
        "code": "REFINED",
        "label": "세련된",
    },
    {
        "code": "MINIMAL",
        "label": "미니멀",
    },
    {
        "code": "CONTEMPORARY",
        "label": "컨템포러리",
    },
    {
        "code": "FEMININE",
        "label": "페미닌",
    },
    {
        "code": "BOLD",
        "label": "볼드",
    },
    {
        "code": "PLAYFUL",
        "label": "플레이풀",
    },
    {
        "code": "CASUAL",
        "label": "캐주얼",
    },
    {
        "code": "URBAN",
        "label": "어반",
    },
    {
        "code": "LUXURIOUS",
        "label": "럭셔리",
    },
    {
        "code": "SPORTY",
        "label": "스포티",
    },
]


class Command(BaseCommand):
    help = "StyleChip 기본 데이터를 생성합니다."

    def handle(self, *args, **options):

        for data in STYLE_CHIPS:
            StyleChip.objects.update_or_create(
                code=data["code"],
                defaults={
                    "label": data["label"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "StyleChip 12개 seed 데이터 생성 완료"
            )
        )