from django.db import models
from django.conf import settings
from products.models import Product


class StyleChip(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True
    )

    label = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.label


class VisitSession(models.Model):
    session_key = models.CharField(
        max_length=100,
        unique=True
    )

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )


class VisitHistory(models.Model):
    visit_session = models.ForeignKey(
        VisitSession,
        on_delete=models.CASCADE,
        related_name="histories"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="visit_histories"
    )
    sequence = models.PositiveIntegerField()
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sequence"]


class StyleProfile(models.Model):
    visit_session = models.ForeignKey(
        VisitSession,
        on_delete=models.CASCADE,
        related_name="style_profiles"
    )

    main_product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="style_profiles",
        # null=True,
        # blank=True,
    )

    summary = models.TextField()

    style_chips = models.ManyToManyField(
        StyleChip,
        related_name="style_profiles"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Look(models.Model):

    class ImageStatus(models.TextChoices):
            PENDING = "PENDING", "Pending"
            PROCESSING = "PROCESSING", "Processing"
            COMPLETED = "COMPLETED", "Completed"
            FAILED = "FAILED", "Failed"

    style_profile = models.ForeignKey(
        StyleProfile,
        on_delete=models.CASCADE,
        related_name="looks"
    )

    style_chip = models.ForeignKey(
        StyleChip,
        on_delete=models.PROTECT,
        related_name="looks"
    )

    look_order = models.PositiveIntegerField()

    title = models.CharField(max_length=100)

    subtitle = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField()

    reason = models.TextField()

    image = models.ImageField(
        upload_to="looks/",
        null=True,
        blank=True
    )

    image_status = models.CharField(
        max_length=20,
        choices=ImageStatus.choices,
        default=ImageStatus.PENDING,
    )

    class Meta:
        ordering = ["look_order"]

        constraints = [
            models.UniqueConstraint(
                fields=["style_profile", "look_order"],
                name="unique_look_order_per_profile"
            ),
            models.UniqueConstraint(
                fields=["style_profile", "style_chip"],
                name="unique_style_chip_per_profile_look"
            ),
        ]




class LookProduct(models.Model):

    class Source(models.TextChoices):
        VISITED = "VISITED", "Visited Product"
        RECOMMENDED = "RECOMMENDED", "AI Recommended"

    look = models.ForeignKey(
        Look,
        on_delete=models.CASCADE,
        related_name="look_products"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="look_products"
    )

    item_type = models.CharField(
        max_length=20,
        choices=Product.Category.choices,
        editable=False
    )

    source = models.CharField(
        max_length=20,
        choices=Source.choices
    )

    def save(self, *args, **kwargs):
        self.item_type = self.product.category
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["look", "product"],
                name="unique_product_per_look"
            ),
            models.UniqueConstraint(
                fields=["look", "item_type"],
                name="unique_item_type_per_look"
            ),
        ]


class SavedProduct(models.Model):
    visit_session = models.ForeignKey(
        VisitSession,
        on_delete=models.CASCADE,
        related_name="saved_products"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="saved_by_sessions"
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-saved_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "visit_session",
                    "product",
                ],
                name="unique_saved_product_per_session"
            )
        ]

    def __str__(self):
        return f"{self.visit_session_id} - {self.product.name}"