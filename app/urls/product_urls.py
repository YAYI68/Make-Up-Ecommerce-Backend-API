from django.urls import path
from app.views import product_views as views

urlpatterns = [
    path("", views.Products.as_view(), name="all-products"),
    path("create/", views.CreateProduct.as_view(), name="create-product"),
    path("<str:pk>/", views.ProductDetail.as_view(), name="product-detail"),
    path("update/<str:pk>/", views.UpdateProduct.as_view(), name="update-product"),
    path("delete/<str:pk>/", views.DeleteProduct.as_view(), name="delete-product"),

]
