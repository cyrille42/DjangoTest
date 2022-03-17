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
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by')
        try:
            product_list = Product.objects.all().order_by(order_by)
        except Exception:
            product_list = Product.objects.all()
        return product_list


def check_number_of_product_left(cart_list, cart_serializer):
    error = ""
    for product_id in cart_list:
        product = Product.objects.get(pk=product_id)
        if product.product_number < cart_serializer.validated_data.get('product').count(product_id):
            error += "The product " + product.product_name + " have only " + str(product.product_number) + " left\n"
    return error


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
            error = check_number_of_product_left(cart_list, cart_serializer)
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            cart_serializer.save()
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Calculate the number of free item in, X buy Y offer, discount
def nb_free_item(special_discount, special_discount_gift, nb_total):
    r = nb_total % (special_discount + special_discount_gift)
    n = (nb_total - r) / (special_discount + special_discount_gift)
    return max(0, r - special_discount) + (n * special_discount_gift)


def changing_paid_stock(product_id_list, total_product):
    for product_id in product_id_list:
        product = Product.objects.get(pk=product_id)
        product_paid = total_product.count(product_id)
        product.product_number = product.product_number - product_paid
        product.save()


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
                total_price = 0
                product_id_list = list(set(cart_serializer.validated_data.get('product')))
                product_paid = []
                for product_id in product_id_list:
                    product = Product.objects.get(pk=product_id)
                    product_count = cart_serializer.validated_data.get('product').count(product_id)
                    discount_price = round(product.price - product.price * product.discount / 100, 2)
                    if product.special_discount > 0:
                        discounted_product = nb_free_item(product.special_discount, product.special_discount_gift, product_count)
                        product_count -= discounted_product
                        if discounted_product != 0:
                            product_paid.append([product_id, 0, 100, discounted_product])
                    product_paid.append([product_id, discount_price, product.discount, product_count])
                    total_price += discount_price * product_count
                ticket_data = {
                    'product_paid': product_paid,
                    'total_amount': total_price
                }
                ticket_serializer = TicketSerializer(data=ticket_data)
                if ticket_serializer.is_valid():
                    error = check_number_of_product_left(product_id_list, cart_serializer)
                    if error:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                    Cart.objects.filter(id=pk).delete()
                    ticket = ticket_serializer.save()
                    changing_paid_stock(product_id_list, cart_serializer.validated_data.get('product'))
                    return Response("Cart deleted and ticket " + str(ticket.id) + " created", status=status.HTTP_201_CREATED)
                return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketList(generics.ListAPIView):
    """
    API endpoint that allows product to be viewed or created.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class TicketDetail(generics.RetrieveDestroyAPIView):
    """
    API endpoint that allows product to be viewed or created.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
