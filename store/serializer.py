from rest_framework import serializers
from .models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "unit_price",
            "inventory",
            "inventory_checker",
            "collection",
        ]

    inventory_checker = serializers.SerializerMethodField(method_name="inventory_check")
    collection = serializers.StringRelatedField()

    def inventory_check(self, product: Product):
        if product.inventory < 10:
            return "Low"
        return "High"
