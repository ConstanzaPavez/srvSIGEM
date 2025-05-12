from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CategoriaDj

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ingrese su usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ingrese su contraseña'
        })
    )
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaDj
        fields = ['nombre_categoria', 'stock']
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }