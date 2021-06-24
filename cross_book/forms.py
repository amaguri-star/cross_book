from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import *


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("zip_code", "address1", "address2", "address3")
        widgets = {
            'zip_code':
                forms.TextInput(
                    attrs={'class': 'p-postal-code', 'placeholder': '記入例:8005543'}
                ),
            'address1':
                forms.Select(
                    attrs={'class': 'p-region-id', 'placeholder': '記入例:福岡県'}
                ),
            'address2':
                forms.TextInput(
                    attrs={'class': 'p-locality p-street-address p-extended-address',
                           'placeholder': '記入例:福岡市中央区赤坂２丁目３１−１'}
                ),
            'address3':
                forms.TextInput(
                    attrs={'class': '', 'placeholder': '記入例:クロスブックビル606号室'}
                )
        }


class EditUserProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'image', 'profile_text')


choices = Category.objects.all().values_list('name', 'name')


class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['user', 'at_created']
        widgets = {
            'name': forms.TextInput(attrs={'class': '', 'placeholder': '商品名を記入してください(必須)'}),
            'explanation': forms.Textarea(attrs={'class': '', 'placeholder': '商品の説明(必須)'}),
            'category': forms.Select(choices=choices),
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['user', 'at_created']
