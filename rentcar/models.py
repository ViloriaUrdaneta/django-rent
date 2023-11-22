from django.db import models

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12)
    name = models.CharField(max_length=255)

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Arriendo(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    costo_diario = models.DecimalField(max_digits=10, decimal_places=2)
    dias = models.IntegerField()

    def costo_total(self):
        return self.costo_diario * self.dias
