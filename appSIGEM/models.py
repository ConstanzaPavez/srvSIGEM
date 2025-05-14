from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm



class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    imagen_perfil = models.ImageField(upload_to='perfiles', null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        help_text='Specific permissions for this user.',
    )

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen_perfil = models.ImageField(upload_to='perfiles/', default='perfiles/default.jpg')
    
    def __str__(self):
        return self.usuario.username  # Esto es solo para mostrar algo legible en el administrador