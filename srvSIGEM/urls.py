from django.contrib import admin
from django.urls import path
from appSIGEM import views  # Asegúrate de que la importación esté correcta
from django.conf.urls.static import static
from django.conf import settings
from appSIGEM.views import gestionar_solicitud
from django.contrib.auth import views as auth_views
from appSIGEM.views import seleccion_masiva_materiales
from appSIGEM.views import detalle_material_admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('', views.index, name='index'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('agregar-tipo-material/', views.agregar_tipo_material, name='agregar_tipo_material'),
    path('agregar-marca/', views.agregar_marca, name='agregar_marca'),
    path('agregar-material/', views.agregar_material, name='agregar_material'),
    path('listar-materiales/', views.listar_materiales, name='listar_materiales'),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-al-carrito/<int:material_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/quitar/<int:material_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),

    path('crear_solicitud/', views.crear_solicitud, name='crear_solicitud'),
    path('mis_solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('solicitudes/<int:solicitud_id>/gestionar/', gestionar_solicitud, name='gestionar_solicitud'),
    path('solicitudes/<str:numero_solicitud>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('cancelar-solicitud/<int:solicitud_id>/', views.cancelar_solicitud, name='cancelar_solicitud'),

    # urls.py
    path('panel_admin/materiales/', views.admin_listar_materiales, name='admin_listar_materiales'),
    path('panel_admin/materiales/<int:pk>/editar/', views.admin_editar_material, name='admin_editar_material'),
    path('panel_admin/materiales/<int:pk>/eliminar/', views.admin_eliminar_material, name='admin_eliminar_material'),

    
    path("reporte_excel/", views.reporte_excel, name="reporte_excel"),

    path('reporte/prestamos/', views.reporte_prestamos, name='reporte_prestamos'),
    path('reporte/prestamos/pdf/', views.exportar_reporte_pdf, name='reporte_prestamos_pdf'),

    path('control_solicitudes/', views.control_admin_solicitud, name='control_solicitudes'),
    path('devoluciones/', views.gestionar_devoluciones, name='gestionar_devoluciones'),
    path('devoluciones/<int:item_id>/', views.gestionar_devolucion, name='gestionar_devolucion'),

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:user_id>/solicitudes/', views.ver_solicitudes_usuario, name='ver_solicitudes_usuario'),

    path('panel-admin/materiales-danados/', views.listar_materiales_danados, name='listar_materiales_danados'),
    path('panel-admin/materiales-danados/reparar/<int:item_id>/', views.reparar_material, name='reparar_material'),
    
    path('verificar-reservas/', views.verificar_reservas_ajax, name='verificar_reservas_ajax'),

    path('seleccion-masiva-materiales/', seleccion_masiva_materiales, name='seleccion_masiva_materiales'),
    
    path('usuarios/desactivar/<int:usuario_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('usuarios/activar/<int:usuario_id>/', views.activar_usuario, name='activar_usuario'),
    path('material/<int:id>/', views.detalle_material, name='detalle_material'),
    path('panel_admin/materiales/<int:pk>/detalle/', detalle_material_admin, name='detalle_material_admin'),

    
    path('panel_admin/materiales/<int:pk>/reactivar/', views.reactivar_material, name='reactivar_material'),

    path('panel_admin/materiales/inactivos/', views.admin_listar_materiales_inactivos, name='admin_listar_materiales_inactivos'),    
    # Recuperación de contraseña personalizada
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='paginas/auth/password_reset_form.html',
        html_email_template_name='paginas/auth/password_reset_email.html', 
        subject_template_name='paginas/auth/password_reset_subject.txt'
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='paginas/auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='paginas/auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='paginas/auth/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('panel/carrusel/', views.editar_carrusel, name='editar_carrusel'),
    path('panel/carrusel/agregar/', views.agregar_slide, name='agregar_slide'),
    path('panel/carrusel/editar/<int:pk>/', views.editar_slide, name='editar_slide'),
    path('panel/carrusel/eliminar/<int:pk>/', views.eliminar_slide, name='eliminar_slide'),



]

# Archivos estáticos y media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
