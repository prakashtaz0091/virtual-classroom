from django.http import JsonResponse
from main.models import ClassRoom
from account.models import User


def all_classes(request):
    all_classes_data = ClassRoom.objects.all()
    return JsonResponse(list(all_classes_data.values()), safe=False)


def all_teachers(request):
    all_teachers_data = User.objects.filter(role="teacher").values(
        "id", "username", "first_name", "last_name"
    )
    return JsonResponse(list(all_teachers_data), safe=False)
