from django.urls import include, path
from rest_framework import routers
from stock import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('product/', views.ProductList.as_view(), name='product-list'),
    path('cart', views.CartCreate.as_view(), name='cart-create'),
]
