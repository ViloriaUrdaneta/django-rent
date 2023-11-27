from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rentcar.serializers import ArriendoSerializer
from rentcar.utils import get_client_ids, getClientSortByLastName, getClientsSortByAmount, getClientsSortByRentExpenses, getClientsWithLessExpense, getCompaniesSortByProfits, getCompaniesWithRentsOver1Week, getCompanyClientsSortByName, newClientRanking
from .models import Arriendo
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.db.models.functions import Coalesce
from datetime import datetime
from rest_framework.decorators import action
    

class TotalAPIView(APIView):
    def get(self, request, month, empresa=None):
        if month is None:
            mes_actual = datetime.now().month
        else:
            mes_actual = int(month)
            
        arriendos_mes_actual = Arriendo.objects.filter(fecha__month=mes_actual)
        
        # Filtrar por empresa si se proporciona
        if empresa is not None:
            arriendos_mes_actual = arriendos_mes_actual.filter(id_empresa=empresa)
        
        arriendos_mes_actual = arriendos_mes_actual.annotate(
            costo_total=ExpressionWrapper(
                F('costo_diario') * F('dias'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        total_arriendos_mes = arriendos_mes_actual.count()
        
        serializer = ArriendoSerializer(arriendos_mes_actual, many=True)
        arriendos_data = serializer.data
        
        data = {
            'total_arriendos_mes': total_arriendos_mes,
            'arriendos_data': arriendos_data,
        }

        return Response(data, status=status.HTTP_200_OK)
    

class ClienteMasArriendosAPIView(APIView):
    def get(self, request, month, empresa=None):
        if month is None:
            mes_actual = datetime.now().month
        else:
            mes_actual = int(month)
            
        arriendos_mes_actual = Arriendo.objects.filter(fecha__month=mes_actual)
        
        # Filtrar por empresa si se proporciona
        if empresa is not None:
            arriendos_mes_actual = arriendos_mes_actual.filter(id_empresa=empresa)
        
        arriendos_mes_actual = arriendos_mes_actual.annotate(
            costo_total=ExpressionWrapper(
                F('costo_diario') * F('dias'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        arriendos_mes_actual = arriendos_mes_actual.values('id_cliente', 'id_cliente__name').annotate(
            total_costo=Sum(ExpressionWrapper(F('costo_diario') * F('dias'), output_field=DecimalField(max_digits=10, decimal_places=2)))
        )

        cliente_mayor_monto = arriendos_mes_actual.order_by('-costo_total').first()
        
        data = {
            'cliente_mayor_monto': cliente_mayor_monto
        }

        return Response(data, status=status.HTTP_200_OK)
    
    
class ClienteMenorArriendosAPIView(APIView):
    def get(self, request, month, empresa=None):
        if month is None:
            mes_actual = datetime.now().month
        else:
            mes_actual = int(month)
            
        arriendos_mes_actual = Arriendo.objects.filter(fecha__month=mes_actual)
        
        # Filtrar por empresa si se proporciona
        if empresa is not None:
            arriendos_mes_actual = arriendos_mes_actual.filter(id_empresa=empresa)
        
        arriendos_mes_actual = arriendos_mes_actual.annotate(
            costo_total=ExpressionWrapper(
                F('costo_diario') * F('dias'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        arriendos_mes_actual = arriendos_mes_actual.values('id_cliente', 'id_cliente__name').annotate(
            total_costo=Sum(ExpressionWrapper(F('costo_diario') * F('dias'), output_field=DecimalField(max_digits=10, decimal_places=2)))
        )

        cliente_menor_monto = arriendos_mes_actual.order_by('costo_total').first()
        
        data = {
            'cliente_menor_monto': cliente_menor_monto
        }

        return Response(data, status=status.HTTP_200_OK)
    
    
class ListaClientesAPIView(APIView):

    def get(self, request):
        cliente_ids = get_client_ids()
        return Response(cliente_ids, status=status.HTTP_200_OK)
    
    
class ListaClientesPorApellidoAPIView(APIView):

    def get(self, request):
        task = getClientSortByLastName()
        return Response(task, status=status.HTTP_200_OK)
    
    
class ListaClientesPorGastoTotalAPIView(APIView):

    def get(self, request):
        task = getClientsSortByRentExpenses()
        return Response(task, status=status.HTTP_200_OK)
    

class ListaClientesPorEmpresaAPIView(APIView):

    def get(self, request):
        task = getCompanyClientsSortByName()
        return Response(task, status=status.HTTP_200_OK)


class ListaClientesPorTotalPorEmpresaAPIView(APIView):

    def get(self, request, id_empresa=None):
        task = getClientsSortByAmount(id_empresa)
        return Response(task, status=status.HTTP_200_OK)    


class ListaCompaniasPorTotalAPIView(APIView):

    def get(self, request):
        task = getCompaniesSortByProfits()
        return Response(task, status=status.HTTP_200_OK)
    

class ListaEmpresasMasUnaSemanaAPIView(APIView):

    def get(self, request):
        task = getCompaniesWithRentsOver1Week()
        return Response(task, status=status.HTTP_200_OK)
    

class ListaEmpresasPeorClienteAPIView(APIView):

    def get(self, request):
        task = getClientsWithLessExpense()
        return Response(task, status=status.HTTP_200_OK)
    
    
class RankingNuevoClienteAPIView(APIView):

    def get(self, request):
        task = newClientRanking()
        return Response(task, status=status.HTTP_200_OK)