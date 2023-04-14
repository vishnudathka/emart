from django.conf import settings
from django.db import models
from django.db.models import Sum,Q,F,Avg
from django.urls import reverse

USER = settings.AUTH_USER_MODEL


class TimestampedModel(models.Model):
    status: models.BooleanField(default=True)
    create_on: models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImageModel(models.Model):
    name = models.CharField(max_length=255)
    path = models.ImageField(upload_to="image/")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ProductImageModel(ImageModel):
    path = models.ImageField(upload_to="product/image/", default="default/product.jpg")


class UnitModel(models.Model):
    name = models.CharField(max_length=128)
    base = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    symbol = models.CharField(max_length=3)
    conversion_rate = models.FloatField(default=1.0)

    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=500)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    discription = models.TextField(max_length=255)
    price = models.FloatField()
    images = models.ManyToManyField(ProductImageModel)
    unit = models.ForeignKey(UnitModel, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, blank=True
    ) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:product_details", args=(self.id))


class StockModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.FloatField()
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)


class CartModel(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    is_checked_out = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    def total(self):
        price = (
            (
                CartItemModel.objects.filter(cart=self, status=True).annotate(
                    item_price=F("quantity") * F("product__price")
                )
            )
            .aggregate(Sum("item_price"))
            .get("item_price__sum")
        )

        return price

    def items(self):
        cart_items = CartItemModel.objects.filter(cart__user=self.user, status=True)
        return cart_items

    @staticmethod
    def get_cart(request, **kwargs):
        user = request.user
        cart, created = CartModel.objects.get_or_create(
            user=user,
            status=True,
            is_checked_out=False,
            **kwargs,
        )
        return cart    


class CartItemModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1.0)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)


class FeedbackModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    is_replied = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("core:feedback_detail", args=(self.id,))


class WishlistModel(TimestampedModel):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    product = models.ManyToManyField(ProductModel)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ReviewModel(TimestampedModel):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    comment = models.TextField(max_length=255)
    rating = models.FloatField()
    images = models.ManyToManyField(ProductImageModel)

    def __str__(self):
        return str(self.product)



class OrderModel(TimestampedModel):
    order_id = models.CharField(max_length=255, unique=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)


class PaymentModel(TimestampedModel): 

    payment_id = models.CharField(max_length=255, unique=True)
    receipt_no = models.CharField(max_length=255, unique=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=64)
    is_captured = models.BooleanField(default=False)
    is_success = models.BooleanField(default=False)


class ContactModel(models.Model) :
    sno =models.AutoField(primary_key=True)
    name =   models.CharField(max_length=255)
    email =  models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)