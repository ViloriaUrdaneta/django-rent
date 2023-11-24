from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from rentcar.serializers import ArriendoSerializer
from .models import Arriendo
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from datetime import datetime
    

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