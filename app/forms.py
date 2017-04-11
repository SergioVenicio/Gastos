from django import forms
from .models import Item, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'salario', 'senha',)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('descricao', 'valor')
