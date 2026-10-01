from django.db import models
import hashlib

# Create your models here.
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class VehiculoVendido(models.Model):
    id_venta = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_venta = models.DateField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    comprador = models.CharField(max_length=150)


#Clase para usuario
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=64)   # SHA-256 produce 64 hex chars

    def set_password(self, raw_password):
        self.password = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()

    def check_password(self, raw_password):
        return self.password == hashlib.sha256(raw_password.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.username