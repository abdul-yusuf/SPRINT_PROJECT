import imp
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from . import models

class UserProfile(admin.StackedInline):
    model = models.UserProfile
    can_delete = False
    verbose_name = 'userprofile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfile,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.Item)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Category)