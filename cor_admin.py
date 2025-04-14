from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline


class BaseModelAdmin(ModelAdmin):
    pass


class BaseTabularInline(TabularInline):
    pass
