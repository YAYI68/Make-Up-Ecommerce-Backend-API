from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, mixins, generics
from rest_framework import status
from datetime import datetime
from app.models import Order, OrderItem, ShippingAddress, Product
from app.serializers import OrderSerializer, OrderItemSerializer, ShippingAddressserializer


class OrderPagination(PageNumberPagination):
    page_size = 3


class AllOrders(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request):
        return self.list(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({"details": "No Order Items"}, status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice'],
        )

        shippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
            shippingPrice=data["shippingPrice"]

        )

        for item in orderItems:
            product = Product.objects.get(_id=item['id'])

            image = ProductImage.objects.get(product=product)

            itemOrder = OrderItems.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=item['qty'],
                price=item['price'],
                image=image[0].url,
            )
            product.countInStock -= item['qty']
            product.save()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or oder.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            message = {'detail': 'UnAuthorized User'}
            return Response(message, status.HTTP_400_BAD_REQUEST)
    except:
        message = {'detail': 'Order does not exist'}
        return Response(message, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrder(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderPaid(request, pk):
    order = Order.objects.get(_id=pk)
    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response({'success': 'Order was paid'})


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderDelivered(request, pk):
    order = Order.objects.get(_id=pk)
    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()
    return Response({'success': 'Order Delivered'})
