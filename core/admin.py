from django.contrib import admin
from core import models


admin.site.register(models.UnitModel)
admin.site.register(models.CategoryModel)
admin.site.register(models.ProductModel)
admin.site.register(models.StockModel)
admin.site.register(models.CartModel)
admin.site.register(models.CartItemModel)
admin.site.register(models.ProductImageModel)
admin.site.register(models.FeedbackModel)
admin.site.register(models.WishlistModel)
admin.site.register(models.ReviewModel)
# admin.site.register(models.OrderModel)
# admin.site.register(models.PaymentModel)
admin.site.register(models.ContactModel)
