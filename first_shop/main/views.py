from math import atan
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from main.utils import pagination
from main.models import Product, Category, ProductAttrs


products_qnt = 20

def main(request: HttpRequest):
    products = pagination(request, Product, products_qnt)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'main/index.html', context)

def product_view(request: HttpRequest, slag):
    current_product = Product.objects.get(id=slag)
    attributes = ProductAttrs.objects.filter(product=current_product)
    context = {
        'product': current_product,
        'attributes': attributes
    }
    return render(request, 'main/product_view.html', context)

def category_view(request: HttpRequest, slag):
    categories = Category.objects.all()
    current_category = Category.objects.get(id=slag)
    products = current_category.products.all()
    products = pagination(request, current_category, products_qnt, False)

    context = {
        'category': current_category,
        'products': products,
        'categories': categories
    }

    return render(request, 'main/category_view.html', context)
