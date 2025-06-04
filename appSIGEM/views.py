from itertools import count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from .forms import CategoriaForm
from .forms import TipoMaterialForm
from .forms import MarcaForm
from .forms import MaterialForm
from .models import Material, Carrito, ItemCarrito, Solicitud, ItemSolicitud, CategoriaDj
from .forms import LoginForm, CrearUsuarioForm
from django.contrib import messages
from .forms import GestionarSolicitudForm
from .forms import SolicitudForm
from .forms import EditarPerfilForm
from .forms import DevolverItemForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from time import timezone
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect



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
    indices = range(9)  # para 9 slides (0 a 8)
    return render(request, 'paginas/inicio/index.html', {'indices': indices})

# Vista de logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista solo para superusuarios: crear nuevo usuario

def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Usuario inactivo hasta verificar correo
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta en SIGEM'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"http://{current_site.domain}/activar/{uid}/{token}/"
            
            message = render_to_string('emails/activar_cuenta.html', {
                'user': user,
                'activation_link': activation_link,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = 'html'  # Enviar como HTML
            email.send()

            return render(request, 'paginas/registro_pendiente_verificacion.html', {
                'email': user.email
            })
    else:
        form = CrearUsuarioForm()

    return render(request, 'paginas/login/crear_usuario.html', {'form': form})


def enviar_correo_confirmacion(user):
    asunto = 'Bienvenido a SIGEM'
    mensaje = f'''
    Hola {user.first_name},

    Tu cuenta en SIGEM ha sido creada correctamente.

    Usuario: {user.username}
    Correo: {user.email}

    Puedes iniciar sesión aquí: http://127.0.0.1:8000/login/

    Saludos,
    Equipo SIGEM
    '''
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    
def enviar_correo_verificacion(request, user):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://{current_site.domain}/activar-cuenta/{uid}/{token}/"

    subject = "Activa tu cuenta en SIGEM"
    message = render_to_string('emails/activar_cuenta.html', {
        'user': user,
        'activation_link': activation_link,
    })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    
def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Cuenta activada correctamente. Ya puedes iniciar sesión.')
        return redirect('login')  # Asegúrate de que exista la URL 'login'
    else:
        return render(request, 'paginas/registro/activacion_invalida.html')
    
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
# Agregar categoría
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría agregada exitosamente.')
            return redirect('agregar_categoria')  # Puedes redirigir a otra vista si prefieres
    else:
        form = CategoriaForm()
    return render(request, 'paginas/agregar_cosas/agregar_categoria.html', {'form': form})


# Agregar tipo de material
def agregar_tipo_material(request):
    if request.method == 'POST':
        form = TipoMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de material agregado exitosamente.')
            return redirect('agregar_tipo_material')
    else:
        form = TipoMaterialForm()
    return render(request, 'paginas/agregar_cosas/agregar_tipo_material.html', {'form': form})


# Agregar marca
def agregar_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca agregada exitosamente.')
            return redirect('agregar_marca')
    else:
        form = MarcaForm()
    return render(request, 'paginas/agregar_cosas/agregar_marca.html', {'form': form})


# Agregar material
def agregar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material agregado exitosamente.')
            return redirect('agregar_material')
    else:
        form = MaterialForm()
    return render(request, 'paginas/agregar_cosas/agregar_material.html', {'form': form})

#listar materiales
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from .models import Material, CategoriaDj


from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .models import Material, CategoriaDj, Carrito, ItemSolicitud

@login_required
def listar_materiales(request):
    hoy = date.today()
    q = request.GET.get('q', '').strip()
    marca = request.GET.get('marca', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    categoria = request.GET.get('categoria', '').strip()

    # Manejo de fechas con sesión
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    
    
    # Si no hay parámetros en GET, limpiar fechas de la sesión
    if not request.GET:
        request.session.pop('fecha_inicio_filtro', None)
        request.session.pop('fecha_fin_filtro', None)

    # Si vienen por GET, actualizar sesión
    if fecha_inicio_str is not None:
        request.session['fecha_inicio_filtro'] = fecha_inicio_str
    else:
        fecha_inicio_str = request.session.get('fecha_inicio_filtro', '')

    if fecha_fin_str is not None:
        request.session['fecha_fin_filtro'] = fecha_fin_str
    else:
        fecha_fin_str = request.session.get('fecha_fin_filtro', '')

    materiales = Material.objects.all()

    # Excluir materiales dañados
    materiales = materiales.exclude(
        itemsolicitud__estado_ingreso='DAN',
        itemsolicitud__fecha_devolucion_real__isnull=False
    )

    # Filtros de búsqueda
    if q:
        materiales = materiales.filter(
            Q(nom_material__icontains=q) |
            Q(marca__nom_marca__icontains=q) |
            Q(categoria__nombre_categoria__icontains=q) |
            Q(tipo_material__nombre_tipo_material__icontains=q)
        )
    if marca:
        materiales = materiales.filter(marca__nom_marca=marca)
    if tipo:
        materiales = materiales.filter(tipo_material__nombre_tipo_material=tipo)
    if categoria:
        materiales = materiales.filter(categoria__nombre_categoria=categoria)

    # Filtro por rango de fechas personalizado usando fecha_inicio_str y fecha_fin_str actualizados
    if fecha_inicio_str and fecha_fin_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()

            materiales_reservados_ids = ItemSolicitud.objects.filter(
                solicitud__estado__in=['PEND', 'APR', 'PAR'],
                solicitud__fecha_retiro__lte=fecha_fin,
                solicitud__fecha_devolucion__gte=fecha_inicio,
                fecha_devolucion_real__isnull=True
            ).values_list('material__id_material', flat=True).distinct()

            materiales = materiales.exclude(id_material__in=materiales_reservados_ids)

        except ValueError:
            pass

    # Info general
    marcas = Material.objects.values_list('marca__nom_marca', flat=True).distinct()
    tipos = Material.objects.values_list('tipo_material__nombre_tipo_material', flat=True).distinct()
    categorias_stock = CategoriaDj.objects.all().order_by('nombre_categoria')

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    materiales_en_carrito = set(item.material.id_material for item in carrito.items.all())

    # Diccionario para mostrar estado visual de reserva actual
    reserva_info = {}
    reservas_activas = ItemSolicitud.objects.filter(
        solicitud__fecha_retiro__lte=hoy,
        fecha_devolucion_real__isnull=True,
        solicitud__fecha_devolucion__gte=hoy,
        solicitud__estado__in=['PEND', 'APR', 'PAR']
    )

    for item in reservas_activas:
        mat_id = item.material.id_material
        estado_solicitud = item.solicitud.estado
        fecha_dev = item.solicitud.fecha_devolucion
        disponible_desde = fecha_dev + timedelta(days=1)

        if hoy <= fecha_dev:
            if estado_solicitud == 'APR':
                reserva_info[mat_id] = f"Disponible desde {disponible_desde.strftime('%d-%m-%Y')}"
            elif estado_solicitud == 'PEND':
                reserva_info[mat_id] = f"Reserva activa"

    return render(request, 'paginas/crud_material/listar_materiales.html', {
        'materiales': materiales,
        'materiales_en_carrito': materiales_en_carrito,
        'reserva_info': reserva_info,
        'marcas': marcas,
        'tipos': tipos,
        'categorias_stock': categorias_stock,
        # Pasar fechas para mostrar en el formulario
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'q': q,
        'marca': marca,
        'tipo': tipo,
        'categoria': categoria,
    })



@login_required
@user_passes_test(is_admin)
def listar_materiales_danados(request):
    # Traer todos los items con estado_ingreso 'DAN'
    items_danados = ItemSolicitud.objects.filter(estado_ingreso='DAN', fecha_devolucion_real__isnull=False)

    return render(request, 'paginas/panel_admin/materiales_danados.html', {
        'items_danados': items_danados
    })


@login_required
@user_passes_test(is_admin)
def reparar_material(request, item_id):
    item = get_object_or_404(ItemSolicitud, id=item_id, estado_ingreso='DAN')
    
    # Cambiar estado_ingreso a 'UTI' (o 'SIN' si prefieres)
    item.estado_ingreso = 'UTI'
    item.save()

    # Sumar stock a la categoría
    categoria = item.material.categoria
    categoria.stock += item.cantidad
    categoria.save()

    messages.success(request, f"Material '{item.material.nom_material}' devuelto a inventario correctamente.")
    return redirect('listar_materiales_danados')



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

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse



@login_required
def agregar_al_carrito(request, material_id):
    if request.method == 'POST':
        material = get_object_or_404(Material, pk=material_id)

#       hoy = date.today()
#
#        esta_solicitado = ItemSolicitud.objects.filter(
#            material=material,
#            solicitud__estado='APR',
#            solicitud__fecha_retiro__lte=hoy,
#            solicitud__fecha_devolucion__gte=hoy,
#            fecha_devolucion_real__isnull=True
#        ).exists()
#
#        if esta_solicitado:
#            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                return JsonResponse({'estado': 'error', 'mensaje': 'Este material ya ha sido solicitado por otra persona y aún no ha sido devuelto.'})
#           messages.warning(request, "Este material ya ha sido solicitado por otra persona y aún no ha sido devuelto.")
#            return redirect('listar_materiales')

        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, material=material)

        if not creado:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'estado': 'error', 'mensaje': 'Este material ya está en tu carrito.'})
            messages.warning(request, "Este material ya está en tu carrito.")
        else:
            item.cantidad = 1
            item.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'estado': 'agregado',
                'url_quitar': reverse('quitar_del_carrito', args=[material_id])
            })

        return redirect('listar_materiales')


@login_required
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    solicitud.estado = 'APR'
    solicitud.save()

    # Actualizar cada material con la fecha de devolución
    for item in solicitud.itemsolicitud_set.all():
        material = item.material
        if solicitud.fecha_devolucion:
            material.reservado_hasta = solicitud.fecha_devolucion
            material.save()




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




from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse

@login_required
def quitar_del_carrito(request, material_id):
    if request.method == 'POST':
        carrito = get_object_or_404(Carrito, usuario=request.user)
        try:
            item = ItemCarrito.objects.get(carrito=carrito, material_id=material_id)
            item.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'estado': 'quitado',
                    'url_agregar': reverse('agregar_al_carrito', args=[material_id])
                })
            messages.success(request, "Material eliminado del carrito.")
            return redirect('listar_materiales')
        except ItemCarrito.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'estado': 'error', 'mensaje': 'Material no encontrado en el carrito.'})
            messages.error(request, "Material no encontrado en el carrito.")
            return redirect('listar_materiales')
    else:
        return JsonResponse({'estado': 'error', 'mensaje': 'Método no permitido'}, status=405)




@login_required
def crear_solicitud(request):
    hoy = now().date()
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    # Obtener fechas desde sesión, si existen
    fecha_inicio_sesion = request.session.get('fecha_inicio_filtro')
    fecha_fin_sesion = request.session.get('fecha_fin_filtro')

    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            fecha_retiro = form.cleaned_data['fecha_retiro']
            fecha_devolucion = form.cleaned_data['fecha_devolucion']

            if not fecha_retiro or not fecha_devolucion:
                messages.error(request, "Debes completar las fechas de retiro y devolución.")
                return redirect('crear_solicitud')

            
            
            # Validar solapamientos para cada material del carrito
            materiales_solapados = []
            for item_carrito in carrito.items.all():
                existe_solapamiento = ItemSolicitud.objects.filter(
                    material=item_carrito.material,
                    solicitud__estado__in=['PEND', 'APR', 'PAR'],
                    fecha_devolucion_real__isnull=True
                ).filter(
                    solicitud__fecha_retiro__lte=fecha_devolucion,
                    solicitud__fecha_devolucion__gte=fecha_retiro,
                ).exists()

                if existe_solapamiento:
                    materiales_solapados.append(item_carrito.material.nom_material)

            if materiales_solapados:
                nombres = ", ".join(materiales_solapados)
                messages.error(request, f"No se puede crear la solicitud porque estos materiales están reservados en las fechas indicadas: {nombres}")
                return redirect('crear_solicitud')

            # Si no hay solapamientos, crear la solicitud
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()

            for item_carrito in carrito.items.all():
                ItemSolicitud.objects.create(
                    solicitud=solicitud,
                    material=item_carrito.material,
                    cantidad=item_carrito.cantidad
                )
            carrito.items.all().delete()

            messages.success(request, "Solicitud enviada correctamente.")
            return redirect('index')

    else:
        # Inicializar el formulario con fechas desde sesión si existen
        initial_data = {}
        if fecha_inicio_sesion:
            initial_data['fecha_retiro'] = fecha_inicio_sesion
        if fecha_fin_sesion:
            initial_data['fecha_devolucion'] = fecha_fin_sesion

        form = SolicitudForm(initial=initial_data)

    return render(request, 'paginas/solicitudes/crear_solicitud.html', {
        'form': form,
        'hoy': hoy,
        'carrito': carrito,
        'items_carrito': carrito.items.all()
    })


    
def listar_solicitudes(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha_solicitud')
    return render(request, 'paginas/solicitudes/listar_solicitudes.html', {'solicitudes': solicitudes})    



def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def gestionar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if not (request.user.is_staff or solicitud.usuario == request.user):
        messages.error(request, 'No tienes permiso para gestionar esta solicitud.')
        return redirect('detalle_solicitud', id=solicitud.id)

    if request.method == 'POST':
        form = GestionarSolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            # Guardar cambios en la solicitud temporalmente
            solicitud_actualizada = form.save(commit=False)

            # Validar stock solo si la solicitud se aprueba
            if solicitud_actualizada.estado == 'APR':
                # Recorremos cada item y comprobamos stock
                for item in solicitud_actualizada.items.all():
                    categoria = item.material.categoria
                    if categoria.stock < item.cantidad:
                        messages.error(request, f"No hay stock suficiente para {item.material.nom_material}. Stock disponible: {categoria.stock}, requerido: {item.cantidad}")
                        return redirect('gestionar_solicitud', solicitud_id=solicitud.id)

            # Guardar la solicitud después de modificar el stock
            solicitud_actualizada.save()

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
        solicitudes = Solicitud.objects.all().order_by('-fecha_solicitud')
    else:
        solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha_solicitud')

    return render(request, 'paginas/solicitudes/listar_solicitudes.html', {
        'solicitudes': solicitudes
    })
    
 
@login_required
def control_admin_solicitud(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('listar_solicitudes')

    estado = request.GET.get('estado', 'PEND').upper()
    
    estados_validos = ['PEND', 'APR', 'PAR', 'RECH', 'FIN']

    if estado in estados_validos:
        solicitudes = Solicitud.objects.filter(estado=estado).order_by('-fecha_solicitud')
    else:
        solicitudes = Solicitud.objects.all().order_by('-fecha_solicitud')

    return render(request, 'paginas/solicitudes/controladminsolicitud.html', {
        'solicitudes': solicitudes,
        'estado_filtrado': estado
    })





@login_required
@user_passes_test(is_admin)
def gestionar_devolucion(request, item_id):
    item = get_object_or_404(ItemSolicitud, id=item_id)
    if request.method == 'POST':
        form = DevolverItemForm(request.POST, instance=item)
        if form.is_valid():
            item_devuelto = form.save(commit=False)

            # Establecer fecha de devolución real como la fecha actual
            item_devuelto.fecha_devolucion_real = now().date()
            item_devuelto.save()

            # Verificar si todos los ítems están devueltos
            solicitud = item_devuelto.solicitud
            hay_no_devuelto = solicitud.items.filter(fecha_devolucion_real__isnull=True).exists()

            if not hay_no_devuelto:
                marcar_solicitud_finalizada(solicitud)

            messages.success(request, "Devolución registrada correctamente.")
            return redirect('gestionar_devoluciones')
    else:
        form = DevolverItemForm(instance=item)

    return render(request, 'paginas/devoluciones/gestionar_devolucion.html', {
        'form': form,
        'item': item
    })
    
    
@login_required
@user_passes_test(is_admin)
def gestionar_devoluciones(request):
    # Cargar todas las solicitudes aprobadas con sus ítems
    solicitudes_aprobadas = Solicitud.objects.filter(estado='APR').prefetch_related('items')

    # Filtrar solo las que tienen al menos un ítem no devuelto
    solicitudes_con_pendientes = [
        solicitud for solicitud in solicitudes_aprobadas
        if solicitud.items.filter(fecha_devolucion_real__isnull=True).exists()
    ]

    # Ordenar por la fecha de devolución planeada (más próxima primero)
    solicitudes_ordenadas = sorted(
        solicitudes_con_pendientes,
        key=lambda s: s.fecha_devolucion or s.fecha_retiro  # fallback si no tiene fecha_devolucion
    )

    return render(request, 'paginas/devoluciones/gestionar_devoluciones.html', {
        'solicitudes': solicitudes_ordenadas
    })

@login_required
@user_passes_test(is_admin)
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'paginas/admin/listar_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(is_admin)
def ver_solicitudes_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    solicitudes = Solicitud.objects.filter(usuario=usuario).order_by('-fecha_solicitud')
    return render(request, 'paginas/admin/solicitudes_usuario.html', {
        'usuario': usuario,
        'solicitudes': solicitudes
    })
    
@login_required
@user_passes_test(is_admin)
def reporte_prestamos(request):
    solicitudes = Solicitud.objects.filter(estado__in=['APR', 'FIN']).select_related('usuario').prefetch_related('items').order_by('-fecha_solicitud')


    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')
    usuario_id = request.GET.get('usuario')

    if fecha_inicio:
        solicitudes = solicitudes.filter(fecha_solicitud__date__gte=fecha_inicio)
    if fecha_fin:
        solicitudes = solicitudes.filter(fecha_solicitud__date__lte=fecha_fin)
    if usuario_id:
        solicitudes = solicitudes.filter(usuario__id=usuario_id)

    usuarios = get_user_model().objects.all()

    context = {
        'solicitudes': solicitudes,
        'usuarios': usuarios,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'usuario_id': usuario_id,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Si es AJAX devolvemos solo el fragmento HTML con los resultados
        return render(request, 'paginas/reportes/_lista_solicitudes.html', context)
    else:
        # Vista normal completa
        return render(request, 'paginas/reportes/reporte_prestamos.html', context)
    
from django.utils.dateparse import parse_date

@login_required
@user_passes_test(is_admin)
def exportar_reporte_pdf(request):
    solicitudes = Solicitud.objects.filter(estado__in=['APR', 'FIN']).select_related('usuario').prefetch_related('items').order_by('-fecha_solicitud')


    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')
    usuario_id = request.GET.get('usuario')

    if fecha_inicio:
        fecha_inicio = parse_date(fecha_inicio)
        if fecha_inicio:
            solicitudes = solicitudes.filter(fecha_solicitud__date__gte=fecha_inicio)

    if fecha_fin:
        fecha_fin = parse_date(fecha_fin)
        if fecha_fin:
            solicitudes = solicitudes.filter(fecha_solicitud__date__lte=fecha_fin)

    if usuario_id and usuario_id.isdigit():
        solicitudes = solicitudes.filter(usuario__id=int(usuario_id))

    # Debug temporal (puedes quitarlo luego)
    print("Total solicitudes encontradas:", solicitudes.count())

    template = get_template('paginas/reportes/reporte_prestamos_pdf.html')
    html = template.render({'solicitudes': solicitudes})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_prestamos.pdf"'

    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8')
    return response

def marcar_solicitud_finalizada(solicitud):
    if solicitud.estado != 'FIN':
        solicitud.estado_anterior = solicitud.estado
        solicitud.estado = 'FIN'
        solicitud.save()


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        perfil_form = EditarPerfilForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if perfil_form.is_valid() and password_form.is_valid():
            perfil_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Mantiene la sesión activa
            messages.success(request, '¡Tu perfil y contraseña se han actualizado correctamente!')
            return redirect('index')  # CORREGIDO: antes decía 'inicio'
    else:
        perfil_form = EditarPerfilForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'paginas/inicio/editar_perfil.html', {
        'perfil_form': perfil_form,
        'password_form': password_form,
    })
    





@login_required
def cancelar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, usuario=request.user)

    if solicitud.estado == 'PEND':
        solicitud.estado = 'CAN'
        solicitud.save()
        messages.success(request, 'Solicitud cancelada exitosamente.')
    else:
        messages.error(request, 'Solo puedes cancelar solicitudes pendientes.')

    return redirect('listar_solicitudes')  # o la vista que estés usando para listarlas
