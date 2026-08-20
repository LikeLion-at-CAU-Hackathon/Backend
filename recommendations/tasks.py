from celery import shared_task

from .models import Look
from .services import generate_look_image


@shared_task
def generate_look_image_task(look_id):
    look = Look.objects.get(id=look_id)

    look.image_status = Look.ImageStatus.PROCESSING
    look.save(
        update_fields=["image_status"]
    )

    try:
        generate_look_image(look)

        look.image_status = Look.ImageStatus.COMPLETED
        look.save(
            update_fields=["image_status"]
        )

        return {
            "look_id": look.id,
            "status": "COMPLETED",
        }

    except Exception as e:
        look.image_status = Look.ImageStatus.FAILED
        look.save(
            update_fields=["image_status"]
        )

        print(
            f"[LOOK IMAGE ERROR] "
            f"look_id={look.id}: {e}"
        )

        raise