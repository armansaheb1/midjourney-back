from rest_framework import routers

from ApiService.viewsets import OrganizationViewSet

router = routers.SimpleRouter()
router.register("organization", OrganizationViewSet, basename="organization")

urlpatterns = router.urls