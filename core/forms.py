from django import forms
from core import models


class ProductForm(forms.ModelForm):
    images = forms.ImageField(required=False)

    class Meta:
        model = models.ProductModel
        fields = ["name", "discription", "price", "unit", "category"]

class FeedbackForm(forms.ModelForm):
    
    class Meta :
        model = models.FeedbackModel
        fields = ["name","email","subject","message"]


class WishlistForm(forms.ModelForm):

    class Meta :
        model = models.WishlistModel
        fields = ["name"] 

class ProductImageForm(forms.ModelForm):

    class Meta:
        model =models.ProductImageModel
        fields =["path"]              

class Reviewform(forms.ModelForm):

    class Meta:
        model =models.ReviewModel
        fields =["comment","rating"]

   

