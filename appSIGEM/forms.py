from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CategoriaDj
from .models import TipoMaterial
from .models import Marca
from .models import Material
from .models import Solicitud
from .models import ItemSolicitud
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django import forms

# Formulario de Login
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
    
class CrearUsuarioForm(UserCreationForm):
    imagen_perfil = forms.ImageField(required=False)

    class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email', 'imagen_perfil', 'password1', 'password2']
        

class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'paginas/login/login.html'
    
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
        
        
        
        

class GestionarSolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['estado', 'comentario_respuesta']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'comentario_respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Comentario opcional'}),
        }        
        
        
from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_retiro', 'fecha_devolucion', 'razon_solicitud', 'ubicacion_solicitud']
        widgets = {
            'fecha_retiro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            
            'razon_solicitud': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Explica brevemente el motivo de esta solicitud',
                'rows': 4, }),
            'ubicacion_solicitud': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación (ej. Laboratorio)'}),
        }

        
        
    # Opcional: validación para que fecha_devolucion > fecha_retiro
    def clean(self):
        cleaned_data = super().clean()
        retiro = cleaned_data.get('fecha_retiro')
        devolucion = cleaned_data.get('fecha_devolucion')

        if retiro and devolucion and devolucion <= retiro:
            raise forms.ValidationError("La fecha de devolución debe ser posterior a la fecha de retiro.")        
        
        
class DevolverItemForm(forms.ModelForm):
    class Meta:
        model = ItemSolicitud
        fields = ['estado_ingreso', 'fecha_devolucion_real', 'observacion']
        widgets = {
            'fecha_devolucion_real': forms.DateInput(attrs={
                'type': 'date',
                'readonly': 'readonly',  # Para que no sea editable
                'class': 'form-control'
            }),
            'observacion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Opcional a menos que esté dañado.',
                'class': 'form-control'
            }),
        }
        help_texts = {
            'observacion': 'Este campo es opcional. Úsalo para detallar el daño si corresponde.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_devolucion_real'].initial = timezone.now().date()

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado_ingreso')
        observacion = cleaned_data.get('observacion')

        if estado == 'DAN' and not observacion:
            self.add_error('observacion', 'Debes ingresar una observación si el material está dañado.')

        return cleaned_data



class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }