"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from AppTicaret.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name='index'),
    path("profile/", profile, name='profile'),
    path("category/", Category, name='category'),
    path("cart/", Cart, name='cart'),
    path("product_detail/<int:product_id>/", ProductDetail, name='product_detail'),
    path("favorite/", Favorites, name='favorite'),
    path("favorite/remove/<int:product_id>/", remove_favorite, name='remove-favorite'),
    path("favorite_toggle/<int:product_id>/", toggle_favorite, name='favorite-toggle'),
    path("add_to_cart/<int:product_id>/", add_to_cart, name='add-to-cart'),
    path("checkout/", checkout, name='checkout'),
    path("order/<int:order_id>/", order_detail, name='order_detail'),
    path("orders/", order_history, name='order_history'),
    path("addresses/", address_list, name='address_list'),
    path("address/add/", add_address, name='add_address'),
    path("address/edit/<int:address_id>/", edit_address, name='edit_address'),
    path("address/delete/<int:address_id>/", delete_address, name='delete_address'),
    path("address/set-default/<int:address_id>/", set_default_address, name='set_default_address'),
    path("track-shipment/", track_shipment, name='track_shipment'),
    
    # Yorum sistemi URL'leri
    path("comment/add/<int:product_id>/", add_comment, name='add_comment'),
    path("comment/edit/<int:comment_id>/", edit_comment, name='edit_comment'),
    path("comment/delete/<int:comment_id>/", delete_comment, name='delete_comment'),
    path("comment/get/<int:product_id>/", get_product_comments, name='get_product_comments'),

    #Authentication URLs
    path("login/", Login, name='login'),
    path("register/", Register, name='register'),
    path("logout/", Logout, name='logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),

    path("set_language/<str:language>", set_language, name="set-language"),
]