from django.contrib import admin
from account_app import models

admin.site.register(models.LocationModel)
admin.site.register(models.AddressModel)
admin.site.register(models.ProfileModel)
