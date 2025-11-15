from django.urls import path
from . import views

app_name = 'boutique'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('produit/<int:pk>/', views.product_detail, name='product_detail'),

    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment_view, name='payment'),
    path('order-success/', views.order_success, name='order_success'),

    path('contact/', views.contact, name='contact'),

    # 👉 Nouvelle route pour voir les produits d’une catégorie
    path('categorie/<str:category_name>/', views.category_products, name='category_products'),
]
