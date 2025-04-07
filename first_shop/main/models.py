import random
from django.db import models

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
