from django.contrib import admin
from django.urls import path
from automotora.views import * 

urlpatterns = [
    path('agregar_cliente_vehiculo/', agregar_cliente_vehiculo, name='agregar_cliente_vehiculo'),
    path('ingresarCliente', ingresarCliente, name='ingresarCliente'),
    path('ingresarVehiculo', ingresarVehiculo, name='ingresarVehiculo'),
    path('agregar_vehiculo_vendido/', agregar_vehiculo_vendido, name='agregar_vehiculo_vendido'),
    path('ingresarVehiculoVendido', ingresarVehiculoVendido, name='ingresarVehiculoVendido'),
    path('listarClientes', listarClientes, name='listarClientes'),
    path('busqueda_cliente/', busqueda_cliente, name='busqueda_cliente'),
    path('buscar/', buscar, name='buscar'),
    path('listarVendidos', listarVendidos, name='listarVendidos'),
    path('listarBorrar', listarBorrar, name='listarBorrar'),
    path('automotora/eliminar_vehiculo', eliminar_vehiculo, name='eliminar_vehiculo'),
    path('validarLogin/', validarLogin, name='validarLogin'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
]
