from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from flujopay_backend_test.app_routines.models import Exercise
from flujopay_backend_test.app_routines.models import ExerciseLog
from flujopay_backend_test.app_routines.models import Routine
from flujopay_backend_test.app_routines.models import RoutineExercise


@admin.register(Exercise)
class ExerciseAdmin(SimpleHistoryAdmin):
    fieldsets = (
        (
            _("Información General"),
            {"fields": ("name", "description")},
        ),
    )
    list_display = ["id", "name", "description"]


@admin.register(Routine)
class RoutineAdmin(SimpleHistoryAdmin):
    fieldsets = (
        (
            _("Información General"),
            {"fields": ("user", "name", "day", "time")},
        ),
    )
    list_display = ["id", "user", "name", "day", "time"]


@admin.register(RoutineExercise)
class RoutineExerciseAdmin(SimpleHistoryAdmin):
    fieldsets = (
        (
            _("Información General"),
            {"fields": ("routine", "exercise", "sets", "reps")},
        ),
    )
    list_display = ["id", "routine", "exercise", "sets", "reps"]


@admin.register(ExerciseLog)
class ExerciseLogAdmin(SimpleHistoryAdmin):
    fieldsets = (
        (
            _("Información General"),
            {"fields": ("routine_exercise",)},
        ),
    )
    list_display = ["id", "routine_exercise"]
    list_filter = ["routine_exercise__routine", "routine_exercise__routine__user"]
