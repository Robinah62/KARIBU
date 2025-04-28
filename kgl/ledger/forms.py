from django.forms import ModelForm
# accessing our models to create corresponding forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
# form called addstock
class AddStockForm(ModelForm):
    #class meta is a helper class
    class Meta:
        model = Stock
        #fields = ['product_name', 'quantity', 'cost', 'supplier_name']
        fields = '__all__'
# form called addsales
class AddSaleForm(ModelForm):
    class Meta:
        model = Sale
        #fields __all__ returns all fields from our models
        fields = '__all__'


class UpdateStockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['received_quantity']

class UserCreation(UserCreationForm):
    class Meta:
        model = Userprofile
        fields = "__all__"
        def save(self, commit=True):
            user = super(UserCreation, self)
            if commit:
                user.is_active = True
                user.is_staff = True
                user.save()
                return user       


class CreditSaleForm(forms.ModelForm):
    class Meta:
        model = CreditSale
        fields = '__all__'  # Include all fields from the CreditSale model
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_dispatch': forms.DateInput(attrs={'type': 'date'}),
        }