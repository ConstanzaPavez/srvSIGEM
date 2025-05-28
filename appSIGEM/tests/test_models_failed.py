# appSIGEM/tests/test_modelo_fallido.py

from django.test import TestCase
from appSIGEM.models import User, PerfilUsuario

class PerfilUsuarioTest(TestCase):
    def test_create_perfil_usuario(self):
        user = User.objects.create_user(username='usuario2', password='pass123')
        perfil = PerfilUsuario.objects.create(usuario=user)
        self.assertEqual(perfil.usuario.username, 'usuario2')
