from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from stock.serializers import UserSerializer, GroupSerializer, ProductSerializer, CartSerializer, TicketSerializer, CartDetailSerializer
from stock.models import Product, Cart, Ticket
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


class CartCreate(generics.ListCreateAPIView):
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
                    error += "The product " + product.product_name + " have only " + str(product.product_number) + " left\n"
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            cart_serializer.save()
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# x = special_discount y = special_discount_gift, count = number total of same product
def nb_free_item(x, y, count):
    r = count % (x + y)
    n = (count - r) / (x + y)
    return max(0, r - x) + (n * y)


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows cart to be updated or deleted.
    """
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        cart_serializer = CartDetailSerializer(data=request.data)
        if cart_serializer.is_valid():
            if cart_serializer.validated_data.get('validation') == True:
                # pas oublie de delete le cart
                total_price = 0
                product_id_list = set(cart_serializer.validated_data.get('product'))
                product_paid = []
                for product_id in product_id_list:
                    product = Product.objects.get(pk=product_id)
                    # handling both discount and special discount
                    product_count = product_id_list.count(product_id)
                    if product.special_discount > 0:
                        discounted_product = nb_free_item(product.special_discount, product.special_discount_gift, product_count)
                        normal_price_product = product_count - discounted_product
                        # [product_id, price paid, discount%, nb__of_time]
                        product_paid.append([product_id, 0, 100, discounted_product])
                        product_paid.append([product_id, product.price, 0, normal_price_product])
                        total_price += product.price * normal_price_product
                    else:
                        product_paid.append([product_id, round(product.price * product.discount / 100, 2), product.discount, product_count])
                        total_price += round(product.price * product.discount / 100, 2) * product_count
                ticket_data = {
                    'product_paid': product_paid,
                    'total_amount': total_price
                }
                ticket_serializer = TicketSerializer(data=ticket_data)
                if ticket_serializer.is_valid():
                    Cart.objects.filter(id=pk).delete()
                    ticket = ticket_serializer.save()
                    return Response("Cart deleted and ticket " + str(ticket.id) + " created", status=status.HTTP_201_CREATED)
            # revérifier les stock avant validation
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketList(generics.ListAPIView):
    """
    API endpoint that allows product to be viewed or created.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
