from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from app.serializers import ProductSerializer, ProductImageSerializer
from rest_framework import filters
from app.products import products

# from django_filters.rest_framework import DjangoFilterBackend

from app.models import Product, ProductImage


class ProductPagination(PageNumberPagination):
    page_size = 9


class Products(mixins.ListModelMixin, generics.GenericAPIView):
    pagination_class = ProductPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price', 'category']

    # def get_queryset(self):
    #     query = self.request.query_params.get('keyword')
    #     if query == None:
    #         query = ""
    #     products = Product.objects.filter(
    #         Q(name__icontains=query) |
    #         Q(price__icontains=query) |
    #         Q(category__icontains=query)
    #     )
    #     return products

    def get(self, request):
        return self.list(request)


class CreateProduct(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = request.user
        product = Product.objects.create(
            user=user,
            name="Product Name",
            price=0,
            countInStock=0,
            category="",
            description="Product Description"
        )
        for _ in range(3):
            ProductImage.objects.create(product=product, image="")
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('keyword')
        if query == None:
            query = ""
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(price__icontains=query))
        return products

    def get(self, request, pk):
        return self.retrieve(request, pk)


class UpdateProduct(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        product = self.get_object()
        data = request.data
        images = data["images"]
        product.name = data['name']
        product.price = data['price']
        product.description = data['description']
        product.category = data['category']
        product.countInStock = data['countInStock']
        for i, productImage in enumerate(product.productimage_set.all()):
            print(productImage.image)
            print(i)
            productImage.image = images[i]
            productImage.save()
        product.save()
        serializer = self.get_serializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteProduct(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        return self.destroy(request, pk)


def createReview(request, pk):
    user = request.user
    data = request.data

    product = Product.objects.get(_id=pk)
    alreadyReview = product.review_set.filter(user=user).exist()

    if alreadyReview:
        message = {'detail': 'Product already reviewed by you'}
        return Response(message, status.HTTP_400_BAD_REQUEST)
    elif data['rating'] == 0:
        message = {'detail': 'Please provide a rating'}
        return Response(message, status.HTTP_400_BAD_REQUEST)
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0

        for i in reviews:
            total += i.rating

        product.rating = total / (len(reviews))
        product.save()

        return Response("Review Added")


@api_view(["PUT"])
def updateProductImage(request, pk):
    imageId = request.data["id"]
    product = Product.objects.get(_id=pk)
    image = product.productimage_set.get(id=imageId)
    image.image = "test2.jpg"
    image.save()
    serializer = ProductImageSerializer(image, many=False)
    return Response(serializer.data)
