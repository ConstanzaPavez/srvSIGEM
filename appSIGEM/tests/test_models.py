from django.test import TestCase
from django.utils import timezone
from appSIGEM.models import User, CategoriaDj, TipoMaterial, Marca, Material

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
