from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def my_profile(request):
    return JsonResponse(
        {
            "id": request.user.id,
            "email": request.user.email,
        }
    )
