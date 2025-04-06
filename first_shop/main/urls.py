from django.urls import path
from main import views

urlpatterns = [
    path('', views.main, name='main'),
    path('product/<slag>', views.product_view, name='product_view'),
    path('category/<slag>', views.category_view, name='category_view'),
]
