from django.urls import path
from main import views

urlpatterns = [
    path('', views.main, name='main'),
    path('product/<slag>', views.product_view, name='product_view'),
]
