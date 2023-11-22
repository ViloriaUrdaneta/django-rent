from rest_framework import routers
from .api import ClienteViewSet, EmpresaViewSet, ArriendoViewSet

router = routers.DefaultRouter()

router.register('api/clientes', ClienteViewSet, 'clientes')
router.register('api/empresas', EmpresaViewSet, 'empresas')
router.register('api/clientes', ArriendoViewSet, 'clientes')


urlpatterns = router.urls