from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from .forms import LoginForm

User = get_user_model()  # Obtiene el modelo de usuario actual de Django

# Función que verifica si el usuario es un superusuario
def is_admin(user):
    return user.is_superuser


class LoginView(View):
    def get(self, request):
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
                # Redirige al panel de administrador si es superusuario
                if user.is_superuser:
                    return redirect('admin_panel')
                # Redirige al índice si es usuario normal
                return redirect('index')
            else:
                # Verifica si el usuario existe en la base de datos
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    # Si el usuario existe pero la contraseña es incorrecta
                    error_message = "La contraseña no es correcta."
                else:
                    # Si el usuario no existe
                    error_message = "El usuario no existe."

                return render(request, 'paginas/login/login.html', {
                    'form': form,
                    'error': error_message
                })
        return render(request, 'paginas/login/login.html', {'form': form})


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
            return render(request, 'paginas/admin/crear_usuario.html', {'error': 'El usuario ya existe'})

        User.objects.create_user(username=username, password=password)
        return redirect('admin_panel')

    return render(request, 'paginas/admin/crear_usuario.html')


# Vista para administrador
@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'paginas/inicio/admin_panel.html')  # Cambié la ruta aquí
