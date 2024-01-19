# app/context_processors.py

from .models import Cart


def cart_unit(request):
    if request.user.is_authenticated:
        cart_unit = Cart.objects.filter(user=request.user).count()
#     else:
#         cart_unit = 0  # Or any default value if the user is not authenticated

        return {'cart_unit': cart_unit}
    else:
        return {}
