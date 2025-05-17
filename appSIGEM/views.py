from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from .forms import LoginForm 
from .forms import CategoriaForm
from .forms import TipoMaterialForm
from .forms import MarcaForm
from .forms import MaterialForm
from .models import Material, Carrito, ItemCarrito, Solicitud, ItemSolicitud
from .models import TipoMaterial
from .forms import LoginForm, CrearUsuarioForm
from django.contrib import messages
from .forms import GestionarSolicitudForm


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
                'error': "Usuario y/o contraseña no válidos."
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
        form = CrearUsuarioForm(request.POST, request.FILES)  # Asegúrate de que el archivo se reciba también
        if form.is_valid():
            user = form.save()  # Guarda el usuario con la imagen incluida si está en el modelo User

            # Mensaje de éxito
            messages.success(request, 'El usuario ha sido creado correctamente.')
            return redirect('admin_panel')  # Redirige al panel de administración
    else:
        form = CrearUsuarioForm()

    return render(request, 'paginas/login/crear_usuario.html', {'form': form})

# Vista para administrador
@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'paginas/inicio/admin_panel.html')

@login_required
def perfil_usuario(request):
    # Asumiendo que tienes un modelo de perfil asociado al usuario
    # Se puede acceder directamente a la imagen de perfil desde el modelo User si es que la has añadido allí
    user = request.user  # Obtén el usuario actualmente autenticado
    return render(request, 'paginas/inicio/perfil.html', {'user': user})

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


def editar_materiales(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('listar_materiales')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'paginas/crud_material/editar_materiales.html', {'form': form})

def eliminar_materiales(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('listar_materiales')
    return render(request, 'paginas/crud_material/eliminar_materiales.html', {'material': material})

def agregar_al_carrito(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, material=material)
    if not creado:
        item.cantidad += 1
    item.save()
    return redirect('listar_materiales')

def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'paginas/carrito/ver_carrito.html', {'carrito': carrito})



def vaciar_carrito(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        ItemCarrito.objects.filter(carrito=carrito).delete()
    except Carrito.DoesNotExist:
        pass  # No hay carrito aún

    return redirect('ver_carrito')  # O a donde quieras redirigir



def crear_solicitud(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items_carrito = carrito.items.all()

        if not items_carrito.exists():
            messages.error(request, "Tu carrito está vacío, no puedes crear una solicitud.")
            return redirect('ver_carrito')

        solicitud = Solicitud.objects.create(usuario=request.user)

        for item in items_carrito:
            ItemSolicitud.objects.create(
                solicitud=solicitud,
                material=item.material,
                cantidad=item.cantidad
            )

        # Vaciar carrito después de crear la solicitud
        items_carrito.delete()

        messages.success(request, "Solicitud creada exitosamente.")
        return redirect('index')  # O donde quieras redirigir

    except Carrito.DoesNotExist:
        messages.error(request, "No tienes carrito activo.")
        return redirect('index')
    
    
def listar_solicitudes(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha_solicitud')
    return render(request, 'paginas/solicitudes/listar_solicitudes.html', {'solicitudes': solicitudes})    



def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def gestionar_solicitud(request, solicitud_id):
    # Obtener la solicitud por id
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    # Verifica si el usuario es admin (staff) o es el propietario de la solicitud
    if not (request.user.is_staff or solicitud.usuario == request.user):
        messages.error(request, 'No tienes permiso para gestionar esta solicitud.')
        return redirect('detalle_solicitud', id=solicitud.id)

    if request.method == 'POST':
        form = GestionarSolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            messages.success(request, 'La solicitud fue actualizada correctamente.')
            return redirect('control_solicitudes')


    else:
        form = GestionarSolicitudForm(instance=solicitud)

    return render(request, 'paginas/solicitudes/gestionar_solicitud.html', {
        'form': form,
        'solicitud': solicitud,
    })

def detalle_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    return render(request, 'paginas/solicitudes/detalle_solicitud.html', {'solicitud': solicitud})

@login_required
def listar_solicitudes(request):
    if request.user.is_staff:
        solicitudes = Solicitud.objects.all()
    else:
        solicitudes = Solicitud.objects.filter(usuario=request.user)

    return render(request, 'paginas/solicitudes/listar_solicitudes.html', {
        'solicitudes': solicitudes
    })
    
 
@login_required
def control_admin_solicitud(request):
    # Por ejemplo, traer todas las solicitudes para que el admin las gestione
    # Si quieres que solo lo vea admin, agregar filtro o permiso aquí
    if not request.user.is_staff:  # o is_superuser si quieres
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('listar_solicitudes')

    solicitudes = Solicitud.objects.all().order_by('-fecha_solicitud')
    
    return render(request, 'paginas/solicitudes/controladminsolicitud.html', {
        'solicitudes': solicitudes,
    })    
    
