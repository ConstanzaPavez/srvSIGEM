from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set', # <-- Agrega esto
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set', # <-- Agrega esto
        help_text='Specific permissions for this user.',
    )

class CategoriaDj(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50, null=False)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre_categoria



class TipoMaterial(models.Model):
    id_tipo_material = models.AutoField(primary_key=True)
    nombre_tipo_material = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre_tipo_material


class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nom_marca = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nom_marca
    
class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    nom_material = models.CharField(max_length=225, null=False)
    contenido_material = models.CharField(max_length=255, null=False)
    img_material = models.ImageField(upload_to='materiales/', null=True, blank=True)
    codigo_barra = models.CharField(max_length=50, null=True, blank=True)
    modelo_material = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    fecha_compra = models.DateField(null=True, blank=True)

    # Relaciones foráneas
    categoria = models.ForeignKey('CategoriaDj', on_delete=models.CASCADE)
    tipo_material = models.ForeignKey('TipoMaterial', on_delete=models.CASCADE)
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_material