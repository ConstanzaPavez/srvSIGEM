from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from .forms import LoginForm 
from .forms import CategoriaForm
from .forms import TipoMaterialForm
from .forms import MarcaForm
from .forms import MaterialForm
from .models import Material
User = get_user_model()  # Obtiene el modelo de usuario actual de Django

# Función que verifica si el usuario es un superusuario
def is_admin(user):
    return user.is_superuser

class LoginView(View):
    def get(self, request):
        # Si el usuario ya está autenticado, redirige a la página correspondiente
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin_panel')  # Redirigir al panel de administrador si es superusuario
            return redirect('index')  # Redirigir al índice si es usuario normal
        
        form = LoginForm()
        return render(request, 'paginas/login/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_panel')
                return redirect('index')
            else:
                # Usuario ingresado pero contraseña incorrecta o usuario inexistente
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    error_message = "La contraseña no es correcta."
                else:
                    error_message = "El usuario no existe."
                return render(request, 'paginas/login/login.html', {
                    'form': form,
                    'error': error_message
                })
        else:
            # Formulario no válido: puede deberse a campos vacíos u otros errores
            return render(request, 'paginas/login/login.html', {
                'form': form,
                'error': "Usuario y/o contraseña no validos."
            })

# Vista del índice
@login_required
def index(request):
    return render(request, 'paginas/inicio/index.html')

# Vista de logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista solo para superusuarios: crear nuevo usuario
@login_required
@user_passes_test(is_admin)
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'paginas/login/crear_usuario.html', {
                'error': 'El usuario ya existe'
            })

        # Crear usuario como NO superusuario ni staff
        User.objects.create_user(username=username, password=password, is_staff=False, is_superuser=False)
        return redirect('admin_panel')

    return render(request, 'paginas/login/crear_usuario.html')

# Vista para administrador
@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'paginas/inicio/admin_panel.html')

#agregar categoria
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_categoria')  # cambiar para redirecionar a otra pagina
    else:
        form = CategoriaForm()
    return render(request, 'paginas/agregar_cosas/agregar_categoria.html', {'form': form})

def agregar_tipo_material(request):
    if request.method == 'POST':
        form = TipoMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_tipo_material')  # puedes cambiar la redirección
    else:
        form = TipoMaterialForm()
    return render(request, 'paginas/agregar_cosas/agregar_tipo_material.html', {'form': form})

def agregar_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_marca')  # redirige a la misma página o a otra
    else:
        form = MarcaForm()
    return render(request, 'paginas/agregar_cosas/agregar_marca.html', {'form': form})

#agregar material
def agregar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('agregar_material')  # o redirige a otra página si lo prefieres
    else:
        form = MaterialForm()
    return render(request, 'paginas/agregar_cosas/agregar_material.html', {'form': form})

#listar materiales
def listar_materiales(request):
    materiales = Material.objects.all()
    return render(request, 'paginas/crud_material/listar_materiales.html', {'materiales': materiales})