from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from pprint import pprint

router = SimpleRouter()

router.register("products", views.ProductViewset)
router.register("collections", views.CollectionViewset)

urlpatterns = [
    path("", include(router.urls)),
]
