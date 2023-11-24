from rest_framework import serializers
from .models import Cliente, Empresa, Arriendo

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'rut', 'name')

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('id', 'name')
        

class ArriendoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arriendo
        fields = ('id_cliente', 'id_empresa', 'costo_diario', 'dias', 'fecha')
        
