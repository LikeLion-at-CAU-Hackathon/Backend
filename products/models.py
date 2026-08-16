from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
class Product(BaseModel):
    name = models.TextField()
    style_no = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    specs = models.JSONField(default=dict, blank=True)
    background = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

class ProductDetail(BaseModel):
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

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
    quantity = models.IntegerField(default=0)
    
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
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "detail"],
                name="unique_branch_detail_stock",
            )
        ]

class BusinessHours(BaseModel):
    open = models.DateTimeField()
    close = models.DateTimeField()
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="business_hours",
    )
    
    

class Material(BaseModel):
    name = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="materials/")
    order = models.IntegerField(default=0)
    careguide = models.JSONField(default=dict)

    class Meta:
        ordering = ["order"]

    
class MaterialProduct(BaseModel):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="materials"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["material", "product"],
                name="unique_material_product"
            )
        ]