from django.core.paginator import Paginator
from core.models import ProductModel, CartModel


def common_data(request):
    products = ProductModel.objects.filter(status=True)
    cart = None
    if request.user.is_authenticated:
        cart = CartModel.get_cart(request)
    context = {
        "cart": cart,
    }
    return context