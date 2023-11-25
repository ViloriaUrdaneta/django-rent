from django.urls import path, include
from rest_framework import routers
from .api import ClienteViewSet, EmpresaViewSet, ArriendoViewSet
from .views import clientes_view, editar_cliente_view, eliminar_cliente, empresas_view, editar_empresa_view, eliminar_empresa, arriendos_view, agregar_arriendo
from .api_views import ClienteMasArriendosAPIView, ClienteMenorArriendosAPIView, ListaClientesAPIView, ListaClientesPorApellidoAPIView, ListaClientesPorEmpresaAPIView, ListaClientesPorGastoTotalAPIView, ListaClientesPorTotalPorEmpresaAPIView, ListaCompaniasPorTotalAPIView, ListaEmpresasMasUnaSemanaAPIView, ListaEmpresasPeorClienteAPIView, RankingNuevoClienteAPIView, TotalAPIView

router = routers.DefaultRouter()

router.register('api/clientes', ClienteViewSet, 'clientes')
router.register('api/empresas', EmpresaViewSet, 'empresas')
router.register('api/arriendos', ArriendoViewSet, 'clientes')


urlpatterns = [
    path('clientes/', clientes_view, name='clientes_view'),
    path('editar_cliente/<int:cliente_id>/', editar_cliente_view, name='editar_cliente'),
    path('eliminar_cliente/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),
    path('empresas/', empresas_view, name='empresas_view'),
    path('editar_empresa/<int:empresa_id>/', editar_empresa_view, name='editar_empresa'),
    path('eliminar_empresa/<int:empresa_id>/', eliminar_empresa, name='eliminar_empresa'),
    path('arriendos/', arriendos_view, name='arriendos_view'),
    path('agregar_arriendo/', agregar_arriendo, name='agregar_arriendo'),
    path('api/total/<int:month>/', TotalAPIView.as_view(), name='total_api'),
    path('api/total/<int:month>/<int:empresa>/', TotalAPIView.as_view(), name='total_api_empresa'),
    path('api/mayorcliente/<int:month>/', ClienteMasArriendosAPIView.as_view(), name='mayor_api'),
    path('api/mayorcliente/<int:month>/<int:empresa>/', ClienteMasArriendosAPIView.as_view(), name='mayor_api_empresa'),
    path('api/menorcliente/<int:month>/', ClienteMenorArriendosAPIView.as_view(), name='menor_api'),
    path('api/menorcliente/<int:month>/<int:empresa>/', ClienteMenorArriendosAPIView.as_view(), name='menor_api_empresa'),
    path('api/clientes/ids/', ListaClientesAPIView.as_view(), name='clientes_ids'),
    path('api/clientes/bylastname/', ListaClientesPorApellidoAPIView.as_view(), name='clientes_lastnames'),
    path('api/clientes/byrent/', ListaClientesPorGastoTotalAPIView.as_view(), name='clientes_rents'),
    path('api/clientes/bycompany/', ListaClientesPorEmpresaAPIView.as_view(), name='clientes_companies'),
    path('api/clientes/byexpenseandcompany/<int:id_empresa>/', ListaClientesPorTotalPorEmpresaAPIView.as_view(), name='clientes_rentsandcompanies'),
    path('api/empresas/byrent/', ListaCompaniasPorTotalAPIView.as_view(), name='companies_rents'),
    path('api/empresas/morethanoneweek/', ListaEmpresasMasUnaSemanaAPIView.as_view(), name='companies_more_one_week'),
    path('api/empresas/worstclient/', ListaEmpresasPeorClienteAPIView.as_view(), name='companies_worst_client'),
    path('api/clientes/newclientranking/', RankingNuevoClienteAPIView.as_view(), name='clientes_companies'),
    path('', include(router.urls)),
]
