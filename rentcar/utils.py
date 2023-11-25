import copy
from django.db import models
from collections import defaultdict
from .models import Arriendo, Cliente, Empresa
from .serializers import ClienteSerializer
from django.db.models import F, ExpressionWrapper, DecimalField, Sum, Count, Min

def get_client_ids():
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    cliente_ids_and_names = [{'id': cliente['id'], 'nombre': cliente['name']} for cliente in serializer.data]
    return cliente_ids_and_names

def getClientSortByLastName():
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    
    apellidos = [cliente['name'].split()[-1] for cliente in serializer.data]
    print(apellidos)
    sorted_clientes = sorted(zip(apellidos, serializer.data), key=lambda x: x[0])
    cliente_ids = [cliente[1]['id'] for cliente in sorted_clientes]

    return cliente_ids

def getClientsSortByRentExpenses():
    
    arriendos = Arriendo.objects.all()

    arriendos = arriendos.annotate(
        costo_total=ExpressionWrapper(
            F('costo_diario') * F('dias'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    arriendos = arriendos.values('id_cliente').annotate(
        total_costo=Sum(ExpressionWrapper(F('costo_diario') * F('dias'), output_field=DecimalField(max_digits=10, decimal_places=2)))
    ).order_by('-total_costo')
    print(arriendos)

    cliente_mayor_monto = Cliente.objects.filter(id__in=[cliente['id_cliente'] for cliente in arriendos])

    client_names = [cliente.name for cliente in cliente_mayor_monto]

    return client_names


def getCompanyClientsSortByName():
    
    arriendos_por_empresa = Arriendo.objects.values('id_empresa__name', 'id_cliente__rut', 'id_cliente__name').distinct()

    empresa_clientes_dict = {}
    
    for arriendo_info in arriendos_por_empresa:
        empresa_name = arriendo_info['id_empresa__name']
        cliente_name = arriendo_info['id_cliente__name']
        cliente_rut = arriendo_info['id_cliente__rut']

        if empresa_name not in empresa_clientes_dict:
            empresa_clientes_dict[empresa_name] = []

        empresa_clientes_dict[empresa_name].append(cliente_rut)

    for empresa_name in empresa_clientes_dict:
        empresa_clientes_dict[empresa_name] = sorted(empresa_clientes_dict[empresa_name])
        
    return empresa_clientes_dict


def getClientsSortByAmount(id_empresa=None):
    clientes_gasto_total = Arriendo.objects.filter(
        id_empresa=id_empresa,
        costo_diario__gt=40000  # Cambié costo_total__gt a costo_diario__gt ya que no hay un campo costo_total en tu modelo
    ).annotate(
        costo_total=ExpressionWrapper(
            F('costo_diario') * F('dias'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).values('id_cliente__rut').annotate(
        total_gastado=Sum('costo_total')
    )

    clientes_list = [{'Rut': cliente['id_cliente__rut'], 'MontoGastado': cliente['total_gastado']} for cliente in clientes_gasto_total]

    clientes_ordenados = sorted(clientes_list, key=lambda x: x['MontoGastado'], reverse=True)

    clientes_dict = {cliente['Rut']: cliente['MontoGastado'] for cliente in clientes_ordenados}

    return clientes_dict



def getCompaniesSortByProfits():
    total_dinero_por_empresa = Arriendo.objects.values('id_empresa__name').annotate(
        total_dinero=Sum(
            ExpressionWrapper(
                F('costo_diario') * F('dias'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )

    empresa_dinero_dict = defaultdict(int)

    for arriendo_info in total_dinero_por_empresa:
        empresa_name = arriendo_info['id_empresa__name']
        total_dinero = arriendo_info['total_dinero']
        empresa_dinero_dict[empresa_name] += total_dinero

    empresas_ordenadas = sorted(empresa_dinero_dict.items(), key=lambda x: x[1])

    return empresas_ordenadas


def getCompaniesWithRentsOver1Week():
    empresas_clientes_count = Arriendo.objects.filter(
        dias__gte= 7
    ).values('id_empresa__name').annotate(
        total_clientes=Count('id_cliente', distinct=True)
    )

    # Crear el diccionario
    empresas_list = [{empresa['id_empresa__name']: empresa['total_clientes']} for empresa in empresas_clientes_count]

    return empresas_list

def getClientsWithLessExpense():
    empresas_clientes_min_profit = Arriendo.objects.values('id_empresa__name').annotate(
        cliente_min_profit=Min('id_cliente', output_field=models.IntegerField())
    )

    empresas_dict = {empresa['id_empresa__name']: empresa['cliente_min_profit'] for empresa in empresas_clientes_min_profit}

    # Devolver el diccionario
    return empresas_dict

def newClientRanking(): 
    
    arriendos = Arriendo.objects.all()
    clientes = Cliente.objects.all()
    
    clientes_copy = copy.deepcopy(clientes)
    arriendos_copy = copy.deepcopy(arriendos)
    nuevo_cliente = Cliente.objects.create(rut='11111111-1', name='Nuevo Cliente Ficticio')
    
    autok_sa = Empresa.objects.get(name='AUTOK S.A')
    
    nuevo_arriendo = Arriendo.objects.create(
        id_cliente=nuevo_cliente,
        id_empresa=autok_sa,
        costo_diario=20000,
        dias=30
    )
    
    ranking = getClientsSortByAmount(id_empresa=autok_sa.id)
    posicion_en_ranking = next((index + 1 for index, cliente in enumerate(ranking) if cliente['Rut'] == '11111111-1'), None)

    # Devolver la posición en el ranking
    return ranking