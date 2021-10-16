from django.contrib import admin

# Register your models here.
from.models import Config, FoodItem, Contact, Order
admin.site.register(FoodItem)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(Config)
