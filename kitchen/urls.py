from django.urls import path
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('customers-orders/', views.CustomerOrders, name='customer-orders'),
    path('active-orders/', views.ActiveOrders, name='active-orders'),
    path('news/', views.News, name='news'),
    path('add-food/', views.Add_food, name='add-food'),
]
