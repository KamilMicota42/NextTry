"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from store.views import (
    store_view,
    cart_view,
    checkout_view,
    details_view,
    favorites_view,
    search_view,
    category_view,
    update_item,
    process_order,
)
from accounts.views import (
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # I don't need one of those, but I don't want duck it up
    path('', include('store.urls')),

    path('', store_view, name="store"),

    path('search', search_view, name="search_view"),
    path('cart/', cart_view, name="cart_view"),
    path('checkout/', checkout_view, name="checkout_view"),
    path('favorites/', favorites_view, name="favorites_view"),
    path('category/<str:cats>', category_view, name="category_view"),
    path('details/<int:pk>/', details_view, name="details_view"),

    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('register/', register_view, name="register_view"),

    path('update_item/', update_item, name="update_item"),
    path('process_order/', process_order, name="process_order"),

    path('captcha/', include('captcha.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
