from django.db import models
from django.urls import reverse
from django.conf import settings
USER = settings.AUTH_USER_MODEL


class LocationModel(models.Model):
    lattitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.lattitude},{self.longitude}"


class AddressModel(models.Model):
    building_name = models.CharField(max_length=120)
    landmark = models.CharField(max_length=64)
    place = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    contry = models.CharField(max_length=64)
    post_office = models.CharField(max_length=64)
    post_code = models.CharField(max_length=8)
    location = models.ForeignKey(
        LocationModel, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        text = f"""
        {self.building_name},
        {self.place},
        {self.post_office}
        {self.district},
        {self.state},
        {self.contry} - {self.post_code}
        """
        return text


class ProfileModel(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        TRANSGENDER = "T", "Transgender"

    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    age = models.IntegerField()
    gender = models.CharField(max_length=3, choices=GenderChoices.choices)
    addresses = models.ManyToManyField(AddressModel,blank=True)
    image = models.ImageField(upload_to="accounts_app/profile/image/", default="default/user.jpg")
    phone = models.CharField(max_length=15)
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self): 
        return reverse("account_app:profile_detail", args=(self.id,)) 
    
