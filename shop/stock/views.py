from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from stock.serializers import UserSerializer, GroupSerializer, ProductSerializer, CartSerializer
from stock.models import Product, Cart


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductList(generics.ListCreateAPIView):
    """
    API endpoint that allows product to be viewed or created.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartCreate(generics.CreateAPIView):
    """
    API endpoint that allows cart to be viewed or created.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        cart_serializer = CartSerializer(data=request.data)
        if cart_serializer.is_valid():
            cart_serializer.username = request.user
            cart_serializer.save()
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

