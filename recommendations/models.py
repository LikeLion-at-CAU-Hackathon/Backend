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