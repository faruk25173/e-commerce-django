from django import template
from main.models import Wishlist
register = template.Library()
@register.filter
def wish_list_view(user):
    wlist = Wishlist.objects.filter(user=user)
    if wlist.exists():
        return wlist
    else:
        return wlist

@register.filter
def wish_count(user):
    products = Wishlist.objects.filter(user=user)
    if products.exists():
        return products.count( )
    else:
        return 0