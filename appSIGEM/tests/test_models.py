from django.test import TestCase
from django.utils import timezone
from appSIGEM.models import User, CategoriaDj, TipoMaterial, Marca, Material, Carrito, ItemCarrito, Solicitud, ItemSolicitud



class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='usuario1', password='pass123')
        self.assertEqual(user.username, 'usuario1')

class CategoriaDjTest(TestCase):
    def test_str_categoria(self):
        cat = CategoriaDj.objects.create(nombre_categoria="Cámaras")
        self.assertEqual(str(cat), "Cámaras")

class TipoMaterialTest(TestCase):
    def test_str_tipo_material(self):
        tipo = TipoMaterial.objects.create(nombre_tipo_material="Lente")
        self.assertEqual(str(tipo), "Lente")

class MarcaTest(TestCase):
    def test_str_marca(self):
        marca = Marca.objects.create(nom_marca="Canon")
        self.assertEqual(str(marca), "Canon")

class MaterialTest(TestCase):
    def test_create_material_y_actualiza_stock(self):
        categoria = CategoriaDj.objects.create(nombre_categoria="Micrófonos")
        tipo = TipoMaterial.objects.create(nombre_tipo_material="Condensador")
        marca = Marca.objects.create(nom_marca="Sony")

        material = Material.objects.create(
            nom_material="Micrófono Sony",
            contenido_material="Micrófono condensador profesional",
            categoria=categoria,
            tipo_material=tipo,
            marca=marca
        )
        categoria.refresh_from_db()
        self.assertEqual(str(material), "Micrófono Sony")
        self.assertEqual(categoria.stock, 1)

class CarritoTest(TestCase):
    def test_total_items_carrito(self):
        user = User.objects.create_user(username='usuario2', password='pass123')
        carrito = Carrito.objects.create(usuario=user)
        categoria = CategoriaDj.objects.create(nombre_categoria="Accesorios")
        tipo = TipoMaterial.objects.create(nombre_tipo_material="Soporte")
        marca = Marca.objects.create(nom_marca="Logitech")
        material = Material.objects.create(
            nom_material="Soporte Cámara",
            contenido_material="Soporte ajustable",
            categoria=categoria,
            tipo_material=tipo,
            marca=marca
        )
        ItemCarrito.objects.create(carrito=carrito, material=material, cantidad=3)
        ItemCarrito.objects.create(carrito=carrito, material=material, cantidad=2)
        self.assertEqual(carrito.total_items(), 5)

class SolicitudTest(TestCase):
    def test_creacion_numero_solicitud_unico(self):
        user = User.objects.create_user(username='usuario3', password='pass123')
        solicitud = Solicitud.objects.create(
            usuario=user,
            razon_solicitud="Uso académico",
            ubicacion_solicitud="Sala 201"
        )
        self.assertIsNotNone(solicitud.numero_solicitud)
        self.assertTrue(solicitud.numero_solicitud.endswith(str(timezone.now().year)))

class ItemSolicitudTest(TestCase):
    def test_str_item_solicitud(self):
        user = User.objects.create_user(username='usuario4', password='pass123')
        categoria = CategoriaDj.objects.create(nombre_categoria="Audio")
        tipo = TipoMaterial.objects.create(nombre_tipo_material="Cable")
        marca = Marca.objects.create(nom_marca="Philips")
        material = Material.objects.create(
            nom_material="Cable HDMI",
            contenido_material="Cable 2 metros",
            categoria=categoria,
            tipo_material=tipo,
            marca=marca
        )
        solicitud = Solicitud.objects.create(
            usuario=user,
            razon_solicitud="Presentación",
            ubicacion_solicitud="Sala 101"
        )
        item = ItemSolicitud.objects.create(
            solicitud=solicitud,
            material=material,
            cantidad=4
        )
        self.assertEqual(str(item), "Cable HDMI x 4")
