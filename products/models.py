from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
class Product(BaseModel):
    name = models.TextField()
    category = models.CharField(max_length=50)
    specs = models.JSONField(default=list, blank=True)
    background = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

class ProductDetail(BaseModel):
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="details"
    )
    
class ProductImage(BaseModel):
    image = models.ImageField(upload_to='images/')
    order = models.IntegerField(default=0)
    
    detail = models.ForeignKey(
        ProductDetail,
        on_delete=models.CASCADE,
        related_name="images",
    )
    
    class Meta:
        ordering = ['order']
    
class Branch(BaseModel):
    name = models.CharField(max_length=50)
    
    latitude = models.FloatField() 
    longitude = models.FloatField() 
    
    def __str__(self):
        return self.name
    
class Stock(BaseModel):
    quantity = models.PositiveIntegerField(default=0)
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="stocks",
    )
    detail = models.ForeignKey(
        ProductDetail,
        on_delete=models.CASCADE,
        related_name="stocks",
    )

class BusinessHours(BaseModel):
    open = models.DateTimeField()
    close = models.DateTimeField()
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="business_hours",
    )