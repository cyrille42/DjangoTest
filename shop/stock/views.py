from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from stock.serializers import UserSerializer, GroupSerializer, ProductSerializer, CartSerializer
from stock.models import Product, Cart
from rest_framework import status
from rest_framework.response import Response


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
    API endpoint that allows cart to be created.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_serializer = CartSerializer(data=request.data, context={'request': request})
        if cart_serializer.is_valid():
            cart_list = cart_serializer.validated_data.get('product').copy()
            cart_list = set(cart_list)
            error = ""
            for product_id in cart_list:
                product = Product.objects.get(pk=product_id)
                if product.product_number < cart_serializer.validated_data.get('product').count(product_id):
                    error += "The product " + product.product_name + " have " + str(product.product_number) + " left\n"
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            cart_serializer.save()
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

