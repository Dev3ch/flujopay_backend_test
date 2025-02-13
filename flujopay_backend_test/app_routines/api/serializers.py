from rest_framework import serializers

from flujopay_backend_test.app_routines.models import Exercise
from flujopay_backend_test.app_routines.models import Routine
from flujopay_backend_test.app_routines.models import RoutineExercise
from flujopay_backend_test.utils.customs_serializers import ModelBaseSerializer


class CRUDRoutineExerciseSerializer(ModelBaseSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=RoutineExercise.objects.all())
    should_delete = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = RoutineExercise
        fields = ["id", "exercise", "sets", "reps", "should_delete", "routine"]
        extra_kwargs = {"routine": {"write_only": True, "required": False}}

    def _validate_id(self, attrs: dict):
        if self.instance is None:
            return

        routine: Routine = self.get_value_from_attrs("menu")
        if routine.pk != self.instance.routine.pk:
            message = (
                f"El 'id:{self.instance.pk}' no pertenece a la rutina 'id:{routine.pk}'"
            )
            raise ValueError({"id": [message]})

    def _validate(self, attrs, error_key=None):
        super()._validate(attrs, "exercises")

    def excluded_fields(self):
        return ["should_delete"]

    def create(self, validated_data: dict) -> RoutineExercise:
        initial_data = self.generate_initial_data(
            validated_data,
            self.excluded_fields(),
        )

        return RoutineExercise.objects.create(**initial_data)

    def update(
        self,
        instance: RoutineExercise,
        validated_data: dict,
    ) -> RoutineExercise:
        excluded_fields = [*self.excluded_fields(), "routine"]
        self.update_fields(instance, validated_data, excluded_fields)

        instance.save()
        return instance


class CRUDRoutineSerializer(ModelBaseSerializer):
    exercises = CRUDRoutineExerciseSerializer(
        many=True,
        allow_empty=False,
    )

    class Meta:
        model = Routine
        fields = ["id", "name", "day", "time", "exercises"]

    def excluded_fields(self):
        return ["exercises"]

    def create(self, validated_data: dict) -> Routine:
        initial_data = self.generate_initial_data(
            validated_data,
            self.excluded_fields(),
        )

        initial_data["user"] = self.context["request"].user
        routine = Routine.objects.create(**initial_data)

        exercises = validated_data.get("exercises", False)
        if exercises is not False:
            serializer_class = CRUDRoutineExerciseSerializer
            self.handle_nested_data(exercises, serializer_class, "routine", routine)

        return routine

    def update(self, instance: Routine, validated_data: dict) -> Routine:
        self.update_fields(instance, validated_data, self.excluded_fields())

        exercises = validated_data.get("exercises", False)
        if exercises is not False:
            serializer_class = CRUDRoutineExerciseSerializer
            self.handle_nested_data_with_should_delete(
                exercises,
                serializer_class,
                "routine",
                instance,
                "exercises",
            )

        instance.save()

        return instance


class ListExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "name", "description"]
