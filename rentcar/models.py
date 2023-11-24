from django.db import models

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Arriendo(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    costo_diario = models.DecimalField(max_digits=10, decimal_places=2)
    dias = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.id_cliente.name} - {self.id_empresa.name}"

    def costo_total(self):
        return self.costo_diario * self.dias
