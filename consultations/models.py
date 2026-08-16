from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ConsultationRequest(BaseModel):
        
    REQUEST_TYPE_CHOICES = [
        ("OTHER", "다른 옵션"),
        ("FITTING", "착용 상담"),
        ("STYLING", "스타일링"),
        ("ETC", "기타"),
    ]
    
    STATUS_CHOICES = [
        ("REQUESTED", "요청"),
        ("IN_PROGRESS", "상담 중"),
        ("COMPLETED", "완료"),
    ]
    
    session = models.ForeignKey(
        "recommendations.VisitSession",
        on_delete=models.PROTECT,
        related_name="consultation_requests",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="consultation_requests",
    )
    
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    message = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="REQUESTED")