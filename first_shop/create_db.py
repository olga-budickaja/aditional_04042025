import random
import urllib.request
from django.core.files.base import ContentFile
from main.models import Product, ProductAttrs, Category
from main.data import products, categories

description_text = "Найкращий вибір для вашого улюбленця. Якість перевірена часом."

category_map = {}
for key, cat_data in categories.items():
    cat, _ = Category.objects.get_or_create(name=cat_data["name"])
    category_map[key] = cat

for i in range(1000):
    prod = random.choice(list(products.values()))
    image_name = prod["img"].split("/")[-1].split("?")[0]
    try:
        try:
            response = urllib.request.urlopen(prod["img"])
            img_data = response.read()
            django_file = ContentFile(img_data, name=image_name)
        except Exception as e:
            django_file = None
            print(f"Don`t loaded image {prod['img']}: {e}")

        new_product = Product.objects.create(
            name=prod["name"],
            price=prod["price"],
            is_top=random.choice([True, False]),
            is_new=random.choice([True, False]),
            image=django_file,
            description=description_text,
        )
        ProductAttrs.objects.create(name="Вага", value="2кг", product=new_product)
        ProductAttrs.objects.create(name="Країна Виробник", value="Україна", product=new_product)
        existing_categories = list(Category.objects.all())
        if existing_categories:
            num_categories = random.randint(1, min(2, len(existing_categories)))
            for category in random.sample(existing_categories, num_categories):
                category.products.add(new_product)
    except Exception as e:
        print(f"Error by create product: {e}")
