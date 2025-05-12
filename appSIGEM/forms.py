from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CategoriaDj
from .models import TipoMaterial
from .models import Marca
from .models import Material
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
#formulario tipo material         
class TipoMaterialForm(forms.ModelForm):
    class Meta:
        model = TipoMaterial
        fields = ['nombre_tipo_material']
        widgets = {
            'nombre_tipo_material': forms.TextInput(attrs={'class': 'form-control'}),
        }        
        
#formulario marca        
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nom_marca']
        widgets = {
            'nom_marca': forms.TextInput(attrs={'class': 'form-control'}),
        }        
#formulario material
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            'nom_material',
            'contenido_material',
            'img_material',
            'codigo_barra',
            'modelo_material',
            'color',
            'fecha_compra',
            'categoria',
            'tipo_material',
            'marca',
        ]
        widgets = {
            'nom_material': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido_material': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barra': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_material': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'tipo_material': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].label_from_instance = lambda obj: obj.nombre_categoria
        self.fields['tipo_material'].label_from_instance = lambda obj: obj.nombre_tipo_material
        self.fields['marca'].label_from_instance = lambda obj: obj.nom_marca