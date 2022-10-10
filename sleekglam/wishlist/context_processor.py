from . models import Wish,WishItem
from .views import _wish_id

def wish_counter(request):
    wish_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            wish = Wish.objects.filter(wish_id=_wish_id(request))
            if request.user.is_authenticated:
                wish_items = WishItem.objects.all().filter(user=request.user)
            else:
              wish_items = WishItem.objects.all().filter(wish=wish[:1])
            for wish_item in wish_items:
                wish_count = wish_count + wish_item.quantity
        except Wish.DoesNotExist:
            wish_count = 0
    return dict(wish_count=wish_count)