from math import atan
from django.forms import ImageField
from django.http import HttpRequest
from django.shortcuts import redirect, render
from bot import send_order_message
from main.forms.comment_form import CommentCreateForm
from main.utils import pagination
from main.models import Comment, Order, Product, Category, ProductAttrs


products_qnt = 20

def main(request: HttpRequest):
    products = pagination(request, Product, products_qnt)
    categories = Category.objects.all()


    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'main/index.html', context)

def product_view(request: HttpRequest, slag):
    current_product = Product.objects.get(id=slag)
    attributes = ProductAttrs.objects.filter(product=current_product)

    if request.method == 'POST':
        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = CommentCreateForm()
    elif request.method == "GET":
        form = CommentCreateForm()

    context = {
        'product': current_product,
        'attributes': attributes,
        'form': form
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

def create_comment(request: HttpRequest):
    if request.method == "POST":
        author = request.POST.get("author")
        text = request.POST.get("text")
        product_id = request.POST.get("product_id")
        image = request.FILES.get("image")

        if text and product_id:
            try:
                product = Product.objects.get(id = product_id)
            except:
                return redirect('product_view', slag=product_id)

            Comment.objects.create(author=author, text = text, product_id = product, image=image)

    return redirect('product_view', slag=product_id)

def create_order(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        product_id = request.POST.get("product_id")

        print(f'name: {name}')
        print(f'phone: {phone}')
        print(f'product_id: {product_id}')

        if name and phone and product_id:
            try:
                product = Product.objects.get(id=product_id)
                product_price = product.price
                product_image_url = product.image.url if product.image else None
                print(f"product_price {product_price}")
                print(f"product_image_url {product_image_url}")
            except Product.DoesNotExist:
                return redirect('product_view', slag=product_id)

            Order.objects.create(
                name=name,
                phone=phone,
                product_id=product,
            )

            send_order_message(name, phone, product.name, product_price, product_image_url)


    return redirect('product_view', slag=product_id)
