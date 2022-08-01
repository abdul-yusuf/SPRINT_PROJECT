from core.models import Category
from .views import *
from django.http import HttpResponse
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', ItemView, name='item-view' ),
    path('item/<slug>/', ItemDetailView, name='item-view' ),
    path('item/cart/<slug>/', add_to_cart, name='add-to-cart' ),
    path('order/', order_summary.as_view(), name='order-summary' ),
    path('order/remove/<slug>', remove_from_cart, name='remove-from-cart' ),
    path('register/', register_request, name='register' ),
    path('login/', login_request, name='login' ),
    path('categories/', category_view, name='category-view' ),
    path('categories/<slug>/', category_detail_view, name='category-detail-view' ),
]