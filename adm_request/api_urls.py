from django.conf.urls import url
from . import views
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .rest_api import UserViewSet, ADMRequestViewSet, \
    ConclusionViewSet, InvestigationViewSet, DocumentViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'adm_requests', ADMRequestViewSet)
router.register(r'conclusions', ConclusionViewSet)
router.register(r'investigations', InvestigationViewSet)
router.register(r'documents', DocumentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]