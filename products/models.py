from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class ProductGroup(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    
class Collection(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    season = models.TextField()
    
class Product(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    price = models.IntegerField(default=0)
    color = models.TextField()
    size = models.TextField()
    
    specs = models.JSONField(default=list, blank=True)
    
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    group = models.ForeignKey(ProductGroup, on_delete=models.PROTECT, related_name='products')
    
class Branch(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    
class Stock(BaseModel):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stocks')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'branch'],
                name='unique_product_branch_stock'
            )
        ]
    
class ProductImage(BaseModel):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/')
    order = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    
    class Meta:
        ordering = ['order']
    
class NFCTag(BaseModel):
    id = models.AutoField(primary_key=True)
    tag_id = models.CharField(max_length=255, unique=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='nfc_tag')



class Story(BaseModel):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='story'
    )
    sections = models.JSONField(default=list, blank=True)
    
class Material(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    name = models.TextField()
    location = models.TextField()
    description = models.TextField()
    image = models.ImageField(
        upload_to='materials/',
        blank=True,
        null=True
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

class CareGuide(BaseModel):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='care_guide'
    )
    contents = models.JSONField(default=list, blank=True)
    
class AIConversation(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ai_conversations'
    )
    question = models.TextField()
    answer = models.TextField()