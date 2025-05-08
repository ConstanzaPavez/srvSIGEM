from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .forms import LoginForm
from .models import User
from django.views import View


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'paginas/login/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_admin:
                    return redirect('admin_panel')
                else:
                    return redirect('user_panel')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
        return render(request, 'login.html', {'form': form})

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def crear_usuario(request):
    if request.method == 'POST':
        # Lógica para crear un nuevo usuario (implementar validaciones)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'crear_usuario.html', {'error': 'Usuario ya existe'})
        user = User.objects.create_user(username=username, password=password, is_admin=False)
        return redirect('admin_panel')
    else:
        return render(request, 'crear_usuario.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'admin_panel.html')

@login_required
def user_panel(request):
    return render(request, 'user_panel.html')

