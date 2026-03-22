"""
URL configuration for Deproke eCommerce project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_views.home, name='home'),
    path('users/', include('users.urls', namespace='users')),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
