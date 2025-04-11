from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main import views

urlpatterns = [
    path('', views.main, name='main'),
    path('product/<slag>', views.product_view, name='product_view'),
    path('category/<slag>', views.category_view, name='category_view'),
    path("create_comment/", views.create_comment, name="create_comment"),
    path("create_order/", views.create_order, name="create_order"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
