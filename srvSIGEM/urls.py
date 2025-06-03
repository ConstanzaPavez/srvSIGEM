from django.contrib import admin
from django.urls import path
from appSIGEM import views  # Asegúrate de que la importación esté correcta
from django.conf.urls.static import static
from django.conf import settings
from appSIGEM.views import gestionar_solicitud
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Ruta al panel de administración de Django
    path('admin/', admin.site.urls),

    # Ruta para el login
    path('login/', views.LoginView.as_view(), name='login'),

    # Ruta de logout (Cerrar sesión)
    path('logout/', views.logout_view, name='logout'),  # Asegúrate de que esta línea esté presente

    # Ruta al panel de administración, solo accesible por superusuario
    path('admin_panel/', views.admin_panel, name='admin_panel'),  # Esta línea debe funcionar correctamente ahora

    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),  # Ruta para crear usuarios

    # Ruta del índice (página de inicio) a la que se redirige el usuario normal después de iniciar sesión
    path('', views.index, name='index'),  # Redirige la URL vacía a la vista del índice
    
    #Ruta del la pagina crear usuario 
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),

    
    #Ruta de la pagina perfil 
     path('perfil/', views.perfil_usuario, name='perfil'),
    
    # Ruta para agregar una nueva categoría
    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),

    # Ruta para agregar un nuevo tipo de material
    path('agregar-tipo-material/', views.agregar_tipo_material, name='agregar_tipo_material'),

    # Ruta para agregar una nueva marca
    path('agregar-marca/', views.agregar_marca, name='agregar_marca'),

    # Ruta para agregar un nuevo material (con imagen y relaciones foráneas)
    path('agregar-material/', views.agregar_material, name='agregar_material'),

    # Ruta para listar todos los materiales registrados en el sistema
    path('listar-materiales/', views.listar_materiales, name='listar_materiales'),
    
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    
    path('agregar-al-carrito/<int:material_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),

    path('crear_solicitud/', views.crear_solicitud, name='crear_solicitud'),

    path('mis_solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),

    path('solicitudes/<int:solicitud_id>/gestionar/', gestionar_solicitud, name='gestionar_solicitud'),
    
    path('solicitudes/<int:id>/', views.detalle_solicitud, name='detalle_solicitud'),

    path('control_solicitudes/', views.control_admin_solicitud, name='control_solicitudes'),

    path('devoluciones/<int:item_id>/', views.gestionar_devolucion, name='gestionar_devolucion'),

    path('devoluciones/', views.gestionar_devoluciones, name='gestionar_devoluciones'),

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    
    path('usuarios/<int:user_id>/solicitudes/', views.ver_solicitudes_usuario, name='ver_solicitudes_usuario'),

    path('reporte/prestamos/', views.reporte_prestamos, name='reporte_prestamos'),

    path('reporte/prestamos/pdf/', views.exportar_reporte_pdf, name='reporte_prestamos_pdf'),

    path('carrito/quitar/<int:material_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    
    path('panel-admin/materiales-danados/', views.listar_materiales_danados, name='listar_materiales_danados'),

    path('panel-admin/materiales-danados/reparar/<int:item_id>/', views.reparar_material, name='reparar_material'),
    
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
     
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('cancelar-solicitud/<int:solicitud_id>/', views.cancelar_solicitud, name='cancelar_solicitud'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)