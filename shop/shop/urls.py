from django.urls import include, path, re_path
from rest_framework import routers
from stock import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# TODO: Mettre les urls dans l'app
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('product/', views.ProductList.as_view(), name='product-list'),
    path('cart/', views.CartCreate.as_view(), name='cart-create'),
    re_path(r'^cart/(?P<pk>[0-9]+)/$', views.CartDetail.as_view(), name='cart-detail'),
    path('ticket/', views.TicketList.as_view(), name='ticket-list'),
]

