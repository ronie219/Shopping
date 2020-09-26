from django.contrib import admin

from .models import *
from .forms import itemAddingForm

class adminItem(admin.ModelAdmin):
    model = Item
    list_display = [
        'name',
        'category',
        'in_stock'
    ]
    form = itemAddingForm


admin.site.register(Item,adminItem)
admin.site.register(Category)
admin.site.register(ItemImage)