from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from pprint import pprint

router = routers.DefaultRouter()

router.register("products", views.ProductViewset, basename="products")
router.register("collections", views.CollectionViewset)

products_routers = routers.NestedDefaultRouter(router, "products", lookup="product")
products_routers.register("reviews", views.ReviewViewSet, basename="product-reviews")

urlpatterns = router.urls + products_routers.urls
