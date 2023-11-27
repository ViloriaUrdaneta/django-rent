from django.shortcuts import render, redirect
import requests
from .chart import generar_grafico
from rentcar.models import Arriendo, Cliente, Empresa
from .forms import ClienteForm, EmpresaForm, ArriendoForm, SeleccionarEmpresaForm


def clientes_view(request):
    
    response = requests.get('http://localhost:8000/api/clientes/')
    
    formulario_cliente = ClienteForm()
    if request.method == 'POST':
        formulario_cliente = ClienteForm(request.POST)
        if formulario_cliente.is_valid():
            nuevo_cliente = formulario_cliente.save()
            return redirect('clientes_view')
        
    if response.status_code == 200:
        data = response.json()
        return render(request, 'clientes.html', {'data': data, 'form': formulario_cliente})
    else:
        return render(request, 'error_template.html')
    
def editar_cliente_view(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    formulario_cliente = ClienteForm(request.POST or None, instance=cliente)
    
    if request.method == 'POST':
        if formulario_cliente.is_valid():
            formulario_cliente.save()
            return redirect('clientes_view')

    return render(request, 'editar_cliente.html', {'form': formulario_cliente})  
    
def eliminar_cliente(request, cliente_id):
    empresa = Cliente.objects.get(id=cliente_id)
    empresa.delete()
    return redirect('clientes_view')  
    
    
def empresas_view(request):

    response = requests.get('http://localhost:8000/api/empresas/')
    
    formulario_empresa = EmpresaForm()
    if request.method == 'POST':
        formulario_empresa = EmpresaForm(request.POST)
        if formulario_empresa.is_valid():
            nueva_empresa = formulario_empresa.save()
            return redirect('empresas_view')

    if response.status_code == 200:
        data = response.json()
        return render(request, 'empresas.html', {'data': data, 'form': formulario_empresa})
    else:
        return render(request, 'error_template.html')
    
def editar_empresa_view(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    formulario_empresa = EmpresaForm(request.POST or None, instance=empresa)
    
    if request.method == 'POST':
        if formulario_empresa.is_valid():
            formulario_empresa.save()
            return redirect('empresas_view')

    return render(request, 'editar_empresa.html', {'form': formulario_empresa})  
    
def eliminar_empresa(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    empresa.delete()
    return redirect('empresas_view')  
    
def arriendos_view(request):
    
    response = requests.get('http://localhost:8000/api/arriendos/')
    
    if response.status_code == 200:
        data = response.json()
    
        response_clientes = requests.get('http://localhost:8000/api/clientes/')
        clientes_data = response_clientes.json()

        response_empresas = requests.get('http://localhost:8000/api/empresas/')
        empresas_data = response_empresas.json()
        
        for arriendo in data:
            arriendo['cliente_nombre'] = next((cliente['name'] for cliente in clientes_data if cliente['id'] == arriendo['id_cliente']), 'Cliente no encontrado')
            arriendo['empresa_nombre'] = next((empresa['name'] for empresa in empresas_data if empresa['id'] == arriendo['id_empresa']), 'Empresa no encontrada')
            
        return render(request, 'arriendos.html', {'data': data})
    else:
        return render(request, 'error_template.html')
    
def agregar_arriendo(request):
    formulario_arriendo = ArriendoForm()

    if request.method == 'POST':
        formulario_arriendo = ArriendoForm(request.POST)
        if formulario_arriendo.is_valid():
            formulario_arriendo.save()
            return redirect('arriendos_view')

    return render(request, 'agregar_arriendo.html', {'form': formulario_arriendo})


def graficos(request):
    grafico =  generar_grafico()
    
    context = {'grafico': grafico}
    
    return render(request, 'graficos.html', context)


def botonera_view(request):
    empresas = Empresa.objects.all() 
    formulario_empresa = SeleccionarEmpresaForm()
    context = {'formulario_empresa': formulario_empresa, 'empresas': empresas}
    return render(request, 'botonera.html', context)