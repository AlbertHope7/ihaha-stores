from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, generics

from .models import Collection, Product, OrderItem, Review
from .serializer import CollectionSerializer, ProductSerializer, ReviewSerializer
from .filters import ProductFilters


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilters

    # no attribute for this context class so we overide this method
    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because there are order items associated with it."
                }
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewset(viewsets.ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it includes one or more products."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
