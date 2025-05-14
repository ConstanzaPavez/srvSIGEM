from django.contrib import admin
from django.urls import path
from appSIGEM import views  # Asegúrate de que la importación esté correcta
from django.conf.urls.static import static
from django.conf import settings
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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
