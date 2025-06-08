from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.utils.timezone import now

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    email = models.EmailField(unique=True, verbose_name='Correo electrónico')

    imagen_perfil = models.ImageField(
        upload_to='imagenes_perfil/',
        null=True,
        blank=True,
        verbose_name='Imagen de perfil'
    )

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

    def __str__(self):
        return self.username
    
class CategoriaDj(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50, null=False)
    stock = models.IntegerField(default=0)

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


@receiver(post_save, sender=Material)
def actualizar_stock_categoria(sender, instance, created, **kwargs):
    if created:
        categoria = instance.categoria
        categoria.stock += 1
        categoria.save()    
        
        
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.usuario}'

    def total_items(self):
        return sum(item.cantidad for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.material.nom_material} x {self.cantidad}'


class Solicitud(models.Model):
    
    ESTADOS = [
        ('PEND', 'Pendiente'),
        ('APR', 'Aprobada'),
        ('PAR', 'Aprobada Parcialmente'),
        ('RECH', 'Rechazada'),
        ('FIN', 'cerrado'),
        ('CAN', 'Cancelada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=5, choices=ESTADOS, default='PEND')
    estado_anterior = models.CharField(max_length=5, choices=ESTADOS[:-1], blank=True, null=True)
    comentario_respuesta = models.TextField(blank=True, null=True)
    fecha_retiro = models.DateField(null=True, blank=True)
    fecha_devolucion = models.DateField(null=True, blank=True)

    razon_solicitud = models.CharField(max_length=255,verbose_name="Razón de la solicitud",null=False,blank=False)

    ubicacion_solicitud = models.CharField(max_length=255,verbose_name="Ubicación de uso",null=False,blank=False)
    
    numero_solicitud = models.CharField(max_length=20,unique=True,editable=False,verbose_name="ID de Solicitud",null=True,  blank=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_solicitud:
            anio_actual = now().year
            cantidad_este_anio = Solicitud.objects.filter(
                numero_solicitud__endswith=f"-{anio_actual}"
            ).count() + 1
            self.numero_solicitud = f"{cantidad_este_anio:03d}-{anio_actual}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Solicitud {self.numero_solicitud} - {self.get_estado_display()}"

    
    
class ItemSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    observacion = models.TextField(blank=True, null=True)
    fecha_devolucion_real = models.DateField(blank=True, null=True)

    ESTADOS_INGRESO = [
        ('SIN', 'Sin daño'),
        ('MIN', 'Daños mínimos'),
        ('UTI', 'Utilizable'),
        ('DAN', 'Dañado'),
       
    ]
    estado_ingreso = models.CharField(max_length=3, choices=ESTADOS_INGRESO, blank=True, null=True)


    def __str__(self):
        return f'{self.material.nom_material} x {self.cantidad}'




