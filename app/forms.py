from django import forms
from .models import Item, Gasto, User

class AuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'senha',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'salario', 'senha',)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('descricao', 'valor')

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ('descricao', 'items', 'quantidade')
