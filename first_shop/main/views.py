from django.http import HttpRequest
from django.shortcuts import render
from main.data import categories, products


def main(request: HttpRequest):
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'main/index.html', context)

def product_view(request: HttpRequest, slag):
    current_product = products[slag]

    context = {
        'product': current_product,
    }

    return render(request, 'main/product_view.html', context)

def category_view(request: HttpRequest, slag):
    current_category = categories[slag]

    context = {
        'category': current_category,
        'products': products,
        'categories': categories
    }

    return render(request, 'main/category_view.html', context)
