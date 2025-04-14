from functools import wraps
from django.contrib import admin
from django.shortcuts import redirect
from main.models import *
from unfold.admin import ModelAdmin, TabularInline
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unfold.contrib.forms.widgets import WysiwygWidget
from django.contrib.admin.filters import ChoicesFieldListFilter
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RelatedDropdownFilter
from django.urls import reverse_lazy
from unfold.decorators import action


class BaseModelAdmin(ModelAdmin):
    pass


class BaseTabularInline(TabularInline):
    pass

class CommentInLine(BaseTabularInline):
    model = Comment
    extra = 1

class HorizontalChoicesFieldListFilter(ChoicesFieldListFilter):
    horizontal = True

class CategoryInline(BaseTabularInline):
    model = Category.products.through
    extra = 1
    verbose_name = "Категорія"
    verbose_name_plural = "Категорії"

def image_preview_decorator(field_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, obj):
            image = getattr(obj, field_name, None)
            if image:
                return format_html(f"<img src='{image.url}' width='100px' height='100px'/>")
            return format_html("<h3 style='color: orange;'>немає зображень</h3>")
        return wrapper
    return decorator

# class ImageInline(BaseTabularInline):
#     model = Image
#     extra = 0


admin.site.register([ProductAttrs, Order])

@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    list_display = ["id", "image_preview", "name", "price", "is_top", "is_new", "show_categories"]
    search_fields = ["id", "name"]
    list_filter = ["is_top", "is_new"]
    list_display_links = ["name", "image_preview"]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    list_filter = [
        ("categories", RelatedDropdownFilter),
        ]
    inlines = [CategoryInline]
    list_filter_submit = True
    @action(
        description="Changelist row action",
        url_path="changelist-row-action",
        attrs={}
    )
    def changelist_row_action(self, request, object_id: int):
        obj = Product.objects.get(id = object_id)
        obj.price += 10
        obj.save()
        return redirect(
          reverse_lazy("admin:main_product_changelist")
        )
    def up_price(self,request, queryset):
        for obj in queryset:
            obj.price += 10
            obj.save()
    actions = [up_price]
    actions_row = ['changelist_row_action']

    @image_preview_decorator('image')
    def image_preview(self, obj):
        pass

    def show_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    show_categories.short_description = "Категорії"

@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    list_display = ["id", "name", "product_dropdown"]
    search_fields = ["id", "name"]
    list_display_links = ["id", "name"]
    filter_horizontal = ("products",)  # Це працює, бо Category має поле 'products'

    def product_dropdown(self, obj):
        products = obj.products.all()
        if not products:
            return format_html("<span style='color: gray;'>немає продуктів</span>")

        options = "".join([f"<option>{p.name}</option>" for p in products])
        dropdown_html = f"""
            <select style='max-width: 200px;'>
                {options}
            </select>
        """
        return mark_safe(dropdown_html)

    product_dropdown.short_description = "Товари"



@admin.register(Comment)
class CommentAdmin(BaseModelAdmin):
    list_display = ["id", "image_preview", "author", "text"]
    search_fields = ["id", "author", "text"]
    list_display_links = ["id", "author", "image_preview"]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    @image_preview_decorator('image')
    def image_preview(self, obj):
        pass
