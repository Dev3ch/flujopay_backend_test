from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from flujopay_backend_test.app_routines.api.serializers import CRUDRoutineSerializer
from flujopay_backend_test.app_routines.api.serializers import ListExerciseSerializer
from flujopay_backend_test.app_routines.models import Exercise
from flujopay_backend_test.app_routines.models import Routine


class RoutineViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUDRoutineSerializer

    def get_queryset(self):
        return Routine.objects.filter(user=self.request.user)


class ExerciseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListExerciseSerializer
    queryset = Exercise.objects.all()
