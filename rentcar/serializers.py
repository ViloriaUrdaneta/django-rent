from rest_framework import serializers
from .models import Cliente, Empresa, Arriendo

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'rut', 'name')

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fiels = ('id', 'name')
        

class ArriendoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arriendo
        fiels = ('id_cliente', 'id_empresa', 'costo_diario', 'dias')
        
