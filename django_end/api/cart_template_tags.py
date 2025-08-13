# from django import template
from django import template
# from api.models import Order

register = template.Library()

from api.models import Order
@register.filter



def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].products.count()
        # print(qs[0].products)
        return 0     