from django import forms
from .models import Cliente, Empresa, Arriendo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'
        
class ArriendoForm(forms.ModelForm):
    class Meta:
        model = Arriendo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArriendoForm, self).__init__(*args, **kwargs)

        # Agregar un campo de selección para usuarios (clientes)
        self.fields['id_cliente'] = forms.ModelChoiceField(
            queryset=Cliente.objects.all(),
            empty_label="Seleccione un cliente"
        )
        self.fields['id_cliente'].label = 'Cliente'

        # Agregar un campo de selección para empresas
        self.fields['id_empresa'] = forms.ModelChoiceField(
            queryset=Empresa.objects.all(),
            empty_label="Seleccione una empresa"
        )
        self.fields['id_empresa'].label = 'Empresa'