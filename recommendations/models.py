from django.db import models
from products.models import Product


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


class StyleProfile(models.Model):
    class AnalysisMode(models.TextChoices):
        BEHAVIOR = "BEHAVIOR", "탐색 행동 기반"
        SINGLE_PRODUCT = "SINGLE_PRODUCT", "단일 제품 기반"

    visit_session = models.OneToOneField(
        VisitSession,
        on_delete=models.CASCADE,
        related_name="style_profile"
    )
    summary = models.TextField()
    tags = models.JSONField(default=list)
    analysis_mode = models.CharField(
        max_length=20,
        choices=AnalysisMode.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)


class StylingResult(models.Model):
    style_profile = models.ForeignKey(
        StyleProfile,
        on_delete=models.CASCADE,
        related_name="styling_results"
    )
    look_order = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    reason = models.TextField()


class StylingItem(models.Model):
    styling_result = models.ForeignKey(
        StylingResult,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField()
    type = models.CharField(max_length=50, blank=True)


class RecommendationResult(models.Model):
    class RecommendationType(models.TextChoices):
        SIMILAR = "SIMILAR", "Similar"
        NEW = "NEW", "New"

    style_profile = models.ForeignKey(
        StyleProfile,
        on_delete=models.CASCADE,
        related_name="recommendations"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=20,
        choices=RecommendationType.choices
    )

    reason = models.TextField()

    score = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["score"]


class SavedProduct(models.Model):
    visit_session = models.ForeignKey(
        VisitSession,
        on_delete=models.CASCADE,
        related_name="saved_products"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["visit_session", "product"],
                name="unique_saved_product_per_session"
            )
        ]