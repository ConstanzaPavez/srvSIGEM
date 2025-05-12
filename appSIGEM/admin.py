from django.contrib import admin
from .models import CategoriaDj, TipoMaterial, Marca, Material

# Registrar los modelos para que aparezcan en el admin de Django
admin.site.register(CategoriaDj)
admin.site.register(TipoMaterial)
admin.site.register(Marca)
admin.site.register(Material)