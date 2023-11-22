from django.contrib import admin
from .models import Cliente, Empresa, Arriendo

admin.site.register(Cliente)
admin.site.register(Empresa)
admin.site.register(Arriendo)
