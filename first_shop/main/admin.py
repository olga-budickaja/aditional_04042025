from django.contrib import admin
from main.models import Product, Category, ProductAttrs, Ads

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductAttrs)
admin.site.register(Ads)
