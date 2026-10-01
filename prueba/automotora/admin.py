from django.contrib import admin

# Register your models here.
from automotora.models import *

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'rut', 'nombre', 'apellidos')
    search_fields = ('rut', 'nombre', 'apellidos')
    ordering = ('id_cliente',)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id_vehiculo', 'marca', 'modelo', 'anio', 'obtener_cliente_id')
    search_fields = ('marca', 'modelo', 'anio', 'cliente__pk')
    ordering = ('id_vehiculo',)

    @admin.display(description='CLIENTE', ordering='cliente_id')
    def obtener_cliente_id(self, obj):
        return obj.cliente_id


@admin.register(VehiculoVendido)
class VehiculoVendidoAdmin(admin.ModelAdmin):
    list_display = ('id_venta', 'obtener_vehiculo_id', 'fecha_venta', 'precio_venta', 'comprador')
    search_fields = ('vehiculo__pk', 'fecha_venta', 'precio_venta', 'comprador')
    ordering = ('id_venta',)

    @admin.display(description='VEHICULO', ordering='vehiculo_id')
    def obtener_vehiculo_id(self, obj):
        return obj.vehiculo_id


admin.site.register(Usuario)