from django.contrib import admin
from django.urls import path
from appSIGEM import views  # Asegúrate de que la importación esté correcta
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    # Ruta al panel de administración de Django
    path('admin/', admin.site.urls),
    # Ruta para el login
    path('login/', views.LoginView.as_view(), name='login'),
    # Ruta de logout (Cerrar sesión)
    path('logout/', views.logout_view, name='logout'),  # Asegúrate de que esta línea esté presente
    # Ruta al panel de administración, solo accesible por superusuario
    path('admin_panel/', views.admin_panel, name='admin_panel'),  # Esta línea debe funcionar correctamente ahora
    # Ruta del índice (página de inicio) a la que se redirige el usuario normal después de iniciar sesión
    path('', views.index, name='index'),  # Redirige la URL vacía a la vista del índice
    
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    
   path('perfil/', views.perfil_usuario, name='perfil'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)