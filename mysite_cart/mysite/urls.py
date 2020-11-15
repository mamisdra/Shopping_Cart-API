from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from core import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),
    path('signup/', core_views.signup, name='signup'),
    path('signin/', core_views.signin, name='signin'),
    path('logout/', core_views.logout_view, name='logout'),
    path('product/', core_views.ProductList.as_view(), name='products'),
    path('cart/', core_views.cart_view, name='cart'),
    url(r'^add/(\d+)', core_views.add_to_cart, name='add_to_cart'), 
    url(r'^remove/(\d+)', core_views.remove_from_cart, name='remove_from_cart'), 
    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)