from django.contrib import admin
from django.utils.datetime_safe import datetime

from core.models import Product, Cart, Entry


class EntryAdmin(admin.ModelAdmin):
    # Overide of the save model
    def save_model(self, request, obj, form, change):
        obj.cart.total += obj.quantity * obj.product.price
        obj.cart.save()
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Entry, EntryAdmin)