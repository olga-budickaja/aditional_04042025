import random
from django.db import models
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+380\d{9}$',
    message="Номер телефону повинен бути у форматі: +380XXXXXXXXX"
)

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    is_top = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/images", blank=True, null=True)
    description = models.TextField()

    def random_discount(self):
        if random.randint(0,1):
            return self.price - self.price*0.1
        return self.price

    def __str__(self):
        return f'{self.name} ({self.id})'

class Category(BaseModel):
    name = models.CharField(max_length=150)
    products = models.ManyToManyField(Product, related_name="categories", blank=True)

    def __str__(self):
        return self.name

class ProductAttrs(BaseModel):
    name = models.CharField(max_length=150)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="attributes")

class Ads(BaseModel):
    text = models.CharField(max_length=512)

class Comment(BaseModel):
    author = models.CharField(max_length=150, blank=True, null=True)
    text = models.TextField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                    related_name="comments")
    image = models.ImageField(upload_to="comments/images", blank=True, null=True)

class AdminData(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

class Order(BaseModel):
    phone = models.CharField(
    max_length=13,
    validators=[phone_validator],
    verbose_name="Телефон"
    )
    name = models.CharField(max_length=100)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                    related_name="orders")

    @property
    def product_name(self):
        return self.product_id.name

    @property
    def product_price(self):
        return self.product_id.price

    @property
    def product_image(self):
        return self.product_id.image.url if self.product_id.image else None
