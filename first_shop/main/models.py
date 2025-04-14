import os
import random
from tabnanny import verbose
from django.db import models
from django.core.validators import RegexValidator

from config.settings import BASE_DIR


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
    name = models.CharField(max_length=255, verbose_name="Назва")
    price = models.FloatField(verbose_name="Ціна")
    is_top = models.BooleanField(default=False, verbose_name="Топ продажів")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    image = models.ImageField(upload_to="products/images", blank=True, null=True, verbose_name="Фото")
    description = models.TextField(verbose_name="Опис")

    def random_discount(self):
        if random.randint(0,1):
            return self.price - self.price*0.1
        return self.price

    def __str__(self):
        return f'{self.name} ({self.id})'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class Category(BaseModel):
    name = models.CharField(max_length=150, verbose_name="Назва")
    products = models.ManyToManyField(Product, related_name="categories", blank=True, verbose_name="Товари")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class ProductAttrs(BaseModel):
    name = models.CharField(max_length=150, verbose_name="Назва")
    value = models.CharField(max_length=255, verbose_name="Значення")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="attributes", verbose_name="Товар")

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибути"

class Ads(BaseModel):
    text = models.CharField(max_length=512)


class Comment(BaseModel):
    author = models.CharField(max_length=150, blank=True, null=True, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                    related_name="comments")
    image = models.ImageField(upload_to="comments/images", blank=True, null=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

class Order(BaseModel):
    phone = models.CharField(
    max_length=13,
    validators=[phone_validator],
    verbose_name="Телефон"
    )
    name = models.CharField(max_length=100, verbose_name="Ім'я")
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

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
