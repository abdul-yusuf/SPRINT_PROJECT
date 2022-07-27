from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Item)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Category)