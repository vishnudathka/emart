from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic as views
from core import models
from django.urls import reverse_lazy
from core import forms
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import mixins as auth_mixins
from .models import ContactModel
from django.views import View
from . import models
    

class HomeView(views.TemplateView):
    template_name = "core/home.html"
    extra_context = {
        "products": models.ProductModel.objects.all(),
        
    }


# this is exagiration of templateview

# class HomeView(views.View):
#     template_name = "core/home.html"
#     def get(self, request, *args):
#         context={
#            "project_name" :"Ecart"

#         }
#         return render(request,self.template_name,context)


class AboutView(views.TemplateView):
    template_name = "core/about.html"


class ContactView(views.TemplateView):
    template_name = "core/contact.html"
    model = models.ContactModel
    context_object_name = "contact"
    

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        instance = self.model(name=name, email=email, subject=subject, message=message)
        instance.save()
        return redirect("core:home")


# class ProductListView(views.ListView):
#     template_name = "core/products/product_list.html"
#     model = models.ProductModel
#     context_object_name = "products"


# this is exagiration of Listview


class ProductListView(views.View):
    template_name = "core/products/product_list.html"
    model = models.ProductModel
    context_object_name = "products"

    def get(self, request, *args):
        products = self.model.objects.all()
        context = {
            "products": products,
            "project_name": "Ecart",
            "page_name": "ProductList",
        }
        return render(request, self.template_name, context)


class ProctCreateView(views.CreateView):
    template_name = "core/products/product_create.html"
    model = models.ProductModel
    form_class = forms.ProductForm
    success_url = reverse_lazy("core:product_list")


# class ProductDetailView(views.DetailView):
#     template_name = "core/products/product_detail.html"
#     model =models.ProductModel
#     context_object_name ="product"


class ProductDetailView(views.View):
    template_name = "core/products/product_detail.html"
    model = models.ProductModel
    context_object_name = "product"

    def get(self, request, pk):
        product = self.model.objects.get(id=pk)
        context = {self.context_object_name: product}
        return render(request, self.template_name, context)


# class ProductUpdateView(views.UpdateView):
#     template_name = "core/products/product_update.html"
#     form_class = forms.ProductForm
#     model = models.ProductModel
#     success_url = reverse_lazy("core:product_list")


class ProductUpdateView(views.View):
    template_name = "core/products/product_update.html"
    model = models.ProductModel
    form_class = forms.ProductForm

    def get(self, request, pk):
        product = self.model.objects.get(id=pk)
        context = {"form": self.form_class(instance=product)}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        product = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=product)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save()
        return redirect(reverse_lazy("core:product_detail", args=(obj.id,)))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})


# class ProductDeleteView(views.DeleteView):
#     template_name = "core/products/product_delete.html"
#     model = models.ProductModel
#     success_url = reverse_lazy("core:product_list")


class ProductDeleteView(views.View):
    template_name = "core/products/product_delete.html"
    model = models.ProductModel
    success_url = reverse_lazy("core:product_list")

    def get(self, request, pk):
        product = self.model.objects.get(id=pk)
        cotext = {"product": product}
        return render(request, self.template_name, cotext)

    def post(self, request, pk):
        product = self.model.objects.get(id=pk)
        product.delete()
        # product.status=False
        # product.save()
        return redirect(self.success_url)


class FeedbackCreateView(views.CreateView):
    template_name = "core/feedback/feedback_create.html"
    model = models.FeedbackModel
    form_class = forms.FeedbackForm

    def form_valid(self, form):
        data = form.cleaned_data
        email_to = [
            data["email"],
        ]
        subject = "Thank you for your valuable feedback."
        message = f"""
        Hi {data['name']},
        we have received your feedback.we are
        so excited to reach you.stay turned.
                  
        Thank & regards
        Ecart team
        """
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, email_to, fail_silently=False)

        return super().form_valid(form)


class FeedbackDetailView(views.DetailView):
    template_name = "core/feedback/feedback_detail.html"
    model = models.FeedbackModel
    context_object_name = "feedback"


class FeedbackListView(views.ListView):
    template_name = "core/products/product_list.html"
    model = models.FeedbackModel
    context_object_name = "Feedback List"


# Wishlist related views
class AddToWishlistView(auth_mixins.LoginRequiredMixin, views.View):
    template_name = "core/wishlist/wishlist_list.html"

    def get(self, request, *args, **kwargs):
        wishlists = models.WishlistModel.objects.filter()
        product_id = kwargs.get("pk")
        product = models.ProductModel.objects.get(id=product_id)

        context = {
            "wishlists": wishlists,
            "product": product,
            "wishlist_form": forms.WishlistForm,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        wishlist_ids = request.POST.getlist("wishlist_id")

        product_id = kwargs.get("pk")
        product = models.ProductModel.objects.get(id=product_id)
        wishlists = models.WishlistModel.objects.filter(id__in=wishlist_ids)
        product.wishlistmodel_set.set(wishlists)

        url = request.META.get("HTTP_REFERER")
        return redirect(url, args=args, kwargs=kwargs)


class WishlistCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = "core/wishlist/wishlist_create.html"
    model = models.WishlistModel
    fields = [
        "name",
    ]
    success_url = reverse_lazy("core:wishlist_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WishlistListView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = "core/wishlist/wishlist_list.html"
    model = models.WishlistModel
    context_object_name = "wishlists"
    extra_context = {"wishlist_form": forms.WishlistForm}


# AddToCart related views


class AddToCartView(views.View):

    def get(self, request, *args, **kwargs): 
        
        cart, cart_created = models.CartModel.objects.get_or_create(
            user=request.user, is_checked_out=False
        )
        product = models.ProductModel.objects.get(id=kwargs.get("pk"))
        cart_item, cart_item_created = models.CartItemModel.objects.get_or_create(
            product=product,
            cart=cart,
        )
        if cart_item_created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1

        cart_item.save()
        url = request.META.get("HTTP_REFERER") 
        return redirect(url)

class AddToCartlistView(views.ListView):
     template_name = "core/cart/cart_list.html"
     model = models.CartItemModel
       

class ReviewCreatView(views.CreateView):
    template_name = "core/review/review_create.html"
    model = models.ReviewModel
    form_class = forms.Reviewform

    def form_valid(self, form):
        image_form = forms.ProductImageForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            image = image_form.save()

        product = models.ProductModel.objects.get(id=self.kwargs.get("pk"))
        form.instance.user = self.request.user
        form.instance.product = product
        review = form.save()
        review.images.set([image])
        review.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("core:review_list", kwargs={"pk": self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "image_form": forms.ProductImageForm,
                "product": models.ProductModel.objects.get(id=self.kwargs.get("pk")),
            }
        )
        return context


class ReviewListView(views.ListView):
    template_name = "core/review/review_list.html"
    model = models.ReviewModel
    context_object_name = "reviews"

    def get_context_data(self):
        review = self.model.objects.filter(product_id=self.kwargs.get("pk"))
        context = {self.context_object_name: review}
        context.update(
            {
                "image_form": forms.ProductImageForm,
                "product": models.ProductModel.objects.get(id=self.kwargs.get("pk")),
                "review": review,
            }
        )
        return context


class FindProductView(views.ListView):
    template_name = "core/products/product_list.html"
    model = models.ProductModel
    context_object_name = "products"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        qs = qs.filter(name__icontains=q)
        return qs
