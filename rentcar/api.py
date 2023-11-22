from .models import Cliente, Empresa, Arriendo
from rest_framework import viewsets, permissions
from .serializers import ClienteSerializer, EmpresaSerializer, ArriendoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ClienteSerializer
    
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EmpresaSerializer
    
class ArriendoViewSet(viewsets.ModelViewSet):
    queryset = Arriendo.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ArriendoSerializer