from django.urls import path
from .views import paymentviews,checkout,success
app_name = 'payments'

urlpatterns = [
    # path('payments/', paymentsviews.as_view(), name='payments'),
    # path('products/payments/', paymentviews, name='payments'),
    # path('products/payments/checkout/', checkout, name='checkout'),
    path('products/<int:pk>/checkout/', checkout, name='checkout'),
    path('payments/success/', success, name='success'),
]