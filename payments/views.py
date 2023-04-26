from django.views import generic as views
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.urls import reverse_lazy
import stripe
from core.models import ProductModel
from core.forms import ProductForm
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY




def paymentviews(request):
    return render(request, "payments/payments.html")

# class paymentsviews(views.TemplateView):
#     template_name="payments/payments.html"

def checkout(request, pk):
    try:
        product = ProductModel.objects.get(id=pk)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price = int(product.price * 100) # Convert to cents
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': product.name,
                              
                           
                        },
                        'unit_amount': price,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/payments/success/',
            cancel_url='http://localhost:8000',
        )
        return redirect(checkout_session.url, code=303)
    except stripe.error.InvalidRequestError as e:
        print('Error creating Stripe session:', str(e))
        return HttpResponse('Error creating Stripe session')
    except ProductModel.DoesNotExist:
        return HttpResponse('Product not found')


def success(request):
    return render(request, "payments/success.html")

