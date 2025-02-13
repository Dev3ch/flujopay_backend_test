from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from flujopay_backend_test.app_routines.api.views import ExerciseViewSet
from flujopay_backend_test.app_routines.api.views import RoutineViewSet
from flujopay_backend_test.app_users.api.views import AuthViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"exercises", ExerciseViewSet, basename="exercises")
router.register(r"routines", RoutineViewSet, basename="routines")

app_name = "api"
urlpatterns = router.urls
