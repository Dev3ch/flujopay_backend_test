from django.db import models

from flujopay_backend_test.app_users.models import User
from flujopay_backend_test.utils import constants
from flujopay_backend_test.utils.customs_models import CustomModel


class Exercise(CustomModel):
    name = models.CharField(verbose_name="Nombre", max_length=100)
    description = models.TextField(verbose_name="Descripción", blank=True, default="")

    def __str__(self):
        return self.name


class Routine(CustomModel):
    DAYS = [
        (constants.MONDAY, constants.MONDAY),
        (constants.TUESDAY, constants.TUESDAY),
        (constants.WEDNESDAY, constants.WEDNESDAY),
        (constants.THURSDAY, constants.THURSDAY),
        (constants.FRIDAY, constants.FRIDAY),
        (constants.SATURDAY, constants.SATURDAY),
        (constants.SUNDAY, constants.SUNDAY),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="routines",
        verbose_name="Usuario",
    )
    name = models.CharField(verbose_name="Nombre", max_length=100)
    day = models.CharField(
        verbose_name="Día",
        choices=DAYS,
        max_length=10,
        default=constants.MONDAY,
    )
    time = models.TimeField(verbose_name="Hora", default="00:00")

    class Meta:
        verbose_name = "Rutina"
        verbose_name_plural = "Rutinas"

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class RoutineExercise(CustomModel):
    routine = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="Rutina",
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        verbose_name="Ejercicio",
        related_name="exercises",
    )
    sets = models.PositiveIntegerField(verbose_name="Series", default=3)
    reps = models.PositiveIntegerField(verbose_name="Repeticiones", default=10)

    class Meta:
        verbose_name = "Ejercicio de Rutina"
        verbose_name_plural = "Ejercicios de Rutina"

    def __str__(self):
        return f"{self.routine.name} - {self.exercise.name}"


class ExerciseLog(CustomModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
        related_name="exercises_logs",
    )
    routine_exercise = models.ForeignKey(
        RoutineExercise,
        on_delete=models.CASCADE,
        verbose_name="Ejercicio de Rutina",
        related_name="exercises_logs",
    )

    def __str__(self):
        return f"{self.user.username} - {self.routine_exercise} - {self.created}"
