from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<str:product_id>/', views.product_update, name='product_update'),
    path('products/delete/<str:product_id>/', views.product_delete, name='product_delete'),
]