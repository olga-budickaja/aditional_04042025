import random
from main.models import Product
from data import products  # імпорт даних
from django.core.files.base import ContentFile
import urllib.request
from django.core.files import File
import os

description_text = "Найкращий вибір для вашого улюбленця. Якість перевірена часом."

for i in range(1000):
    prod = random.choice(list(products.values()))

    image_name = prod["img"].split("/")[-1].split("?")[0]

    try:
        response = urllib.request.urlopen(prod["img"])
        img_data = response.read()
        django_file = ContentFile(img_data, name=image_name)

        Product.objects.create(
            name=prod["name"],
            price=prod["price"],
            is_top=random.choice([True, False]),
            is_new=random.choice([True, False]),
            image=django_file,
            description=description_text,
        )
    except Exception as e:
        print(f"Помилка при завантаженні {prod['img']}: {e}")
