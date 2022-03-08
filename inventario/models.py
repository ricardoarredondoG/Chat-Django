from django.db import models

# Create your models here.

class Presentacion (models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre

class ViaAdministracion (models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class PrincipioActivo (models.Model):
    nombre = models.CharField(max_length=200)
    alertaStockBajo = models.IntegerField()
    def __str__(self):
        return self.nombre


class Medicamento(models.Model):
    codigo = models.CharField(max_length=200)
    nombreComercial = models.CharField(max_length=100)
    contraIndicaciones = models.TextField()
    presentacion = models.ForeignKey(Presentacion,  on_delete = models.CASCADE, null=True)
    viaAdministracion = models.ForeignKey(ViaAdministracion,  on_delete = models.CASCADE, null=True)
    PrincipioActivo = models.ForeignKey(PrincipioActivo, on_delete = models.CASCADE, null=True)

class Stock(models.Model):
    nLote = models.IntegerField()
    fecha_vencimiento = models.DateField()
    medicamento = models.ForeignKey(Medicamento, on_delete = models.CASCADE, null=True)
    cantidad = models.IntegerField()
