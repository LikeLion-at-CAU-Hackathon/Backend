from django.core.management.base import BaseCommand

from recommendations.models import StyleChip


STYLE_CHIPS = [
    {
        "code": "CLASSIC",
        "label": "Classic",
    },
    {
        "code": "HERITAGE",
        "label": "Heritage",
    },
    {
        "code": "REFINED",
        "label": "Refined",
    },
    {
        "code": "MINIMAL",
        "label": "Minimal",
    },
    {
        "code": "CONTEMPORARY",
        "label": "Contemporary",
    },
    {
        "code": "FEMININE",
        "label": "Feminine",
    },
    {
        "code": "BOLD",
        "label": "Bold",
    },
    {
        "code": "PLAYFUL",
        "label": "Playful",
    },
    {
        "code": "CASUAL",
        "label": "Casual",
    },
    {
        "code": "URBAN",
        "label": "Urban",
    },
    {
        "code": "LUXURIOUS",
        "label": "Luxurious",
    },
    {
        "code": "SPORTY",
        "label": "Sporty",
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