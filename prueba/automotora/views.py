from functools import wraps
from django.db import IntegrityError, transaction
from django.shortcuts import render
from django.http import HttpResponse
from automotora.models import *
from decimal import Decimal, InvalidOperation
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.db import IntegrityError


# Create your views here.
def requiere_sesion(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


def login_view(request):
    if request.session.get('usuario_id'):
        return redirect('home_page')
    return render(request, 'automotora/login.html')


@requiere_sesion
def index(request):
    return render(request, 'automotora/index.html')


@requiere_sesion
def home_page(request):
    return render(request, 'automotora/index.html')


@requiere_sesion
def agregar_cliente_vehiculo(request):
    return render(request, 'automotora/agregar_cliente_vehiculo.html')


@requiere_sesion
def agregar_vehiculo_vendido(request):
    return render(request, 'automotora/agregar_vehiculo_vendido.html')


@requiere_sesion
def busqueda_cliente(request):
    return render(request,
                  "automotora/busqueda_cliente.html",{"busqueda_realizada":False})

@requiere_sesion
def ingresarCliente(request):
    rut = request.GET.get("txt_rut_cliente", "").strip()
    nombre = request.GET.get("txt_nombre_cliente", "").strip()
    apellidos = request.GET.get("txt_apellidos_cliente", "").strip()

    if not rut or not nombre or not apellidos or len(rut) > 12 or len(nombre) > 100 or len(apellidos) > 150:
        mensaje = "Debe ingresar todos los campos de cliente respetando sus longitudes máximas."
        tipo_mensaje = "error"
    else:
        try:
            with transaction.atomic():
                Cliente.objects.create(rut=rut, nombre=nombre, apellidos=apellidos)
        except IntegrityError:
            mensaje = "Ya existe un cliente registrado con ese RUT."
            tipo_mensaje = "error"
        else:
            mensaje = "Cliente guardado correctamente."
            tipo_mensaje = "success"

    return render(request, "automotora/resultado_operacion.html", {
        "mensaje": mensaje,
        "tipo_mensaje": tipo_mensaje,
    })

#@requiere_sesion
#def ingresarVehiculo(request):
#    marca = request.GET["txt_marca_vehiculo"]
#    modelo = request.GET["txt_modelo_vehiculo"]
#    anio = request.GET["txt_anio_vehiculo"]
#    cliente = request.GET["txt_id_cliente"]
#    if len(marca)>0 and len(marca)<=50 and len(modelo)>0 and len(modelo)<=50 and len(anio)>0 and len(cliente)>0:
#        vehiculo = Vehiculo(
#            marca = marca,
#            modelo = modelo,
#            anio = anio,
#            cliente = Cliente.objects.get(id_cliente=cliente)
#        )
#        vehiculo.save()
#        mensaje='<h2>Vehiculo guardado</h2> <br> <a href="/">Inicio</a>'
#    else:
#        mensaje='<h2>Debe ingresar todos los campos de vehiculo</h2><br><a href="/">Inicio</a>'
#    return HttpResponse(mensaje)



@requiere_sesion
def ingresarVehiculo(request):
    marca = request.GET.get("txt_marca_vehiculo", "").strip()
    modelo = request.GET.get("txt_modelo_vehiculo", "").strip()
    anio = request.GET.get("txt_anio_vehiculo", "").strip()
    cliente_id = request.GET.get("txt_id_cliente", "").strip()

    # Validación de campos vacíos y longitudes máximas (mismo patrón que Cliente)
    if (not marca or len(marca) > 50 or
            not modelo or len(modelo) > 50 or
            not anio or
            not cliente_id):
        mensaje = "Debe ingresar todos los campos del vehículo respetando sus longitudes máximas."
        tipo_mensaje = "error"
    else:
        try:
            with transaction.atomic():
                # Validar que exista el cliente asociado
                cliente = Cliente.objects.get(id_cliente=cliente_id)
                Vehiculo.objects.create(
                    marca=marca,
                    modelo=modelo,
                    anio=anio,
                    cliente=cliente,
                )
        except Cliente.DoesNotExist:
            mensaje = "El cliente indicado no existe. Verifique el ID ingresado."
            tipo_mensaje = "error"
        except (IntegrityError, ValueError):
            mensaje = "No fue posible guardar el vehículo. Verifique los datos ingresados."
            tipo_mensaje = "error"
        else:
            mensaje = "Vehículo guardado correctamente."
            tipo_mensaje = "success"

    return render(request, "automotora/resultado_operacion.html", {
        "mensaje": mensaje,
        "tipo_mensaje": tipo_mensaje,
    })



#@requiere_sesion
#def ingresarVehiculoVendido(request):
#    vehiculo_id = request.GET.get("txt_id_vehiculo", "").strip()
#    fecha_venta = request.GET.get("txt_fecha_venta", "").strip()
#    precio_venta = request.GET.get("txt_precio_venta", "").strip()
#    comprador = request.GET.get("txt_comprador", "").strip()
#
#    try:
#        precio = Decimal(precio_venta)
#        dos_decimales = precio == precio.quantize(Decimal('0.01'))
#    except (InvalidOperation, ValueError):
#        dos_decimales = False
#
#    if (vehiculo_id and fecha_venta and precio_venta and comprador
#            and len(precio_venta) <= 10 and len(comprador) <= 150 and dos_decimales):
#
#        # 1) Comprobar que el vehículo existe
#        try:
#            vehiculo_obj = Vehiculo.objects.get(id_vehiculo=vehiculo_id)
#        except Vehiculo.DoesNotExist:
#            return HttpResponse('<h2>El vehículo indicado no existe</h2><br><a href="/">Inicio</a>')
#
#        # 2) Comprobar que NO esté ya vendido
#        if VehiculoVendido.objects.filter(vehiculo=vehiculo_obj).exists():
#            return HttpResponse('<h2>Ese vehículo ya fue vendido</h2><br><a href="/">Inicio</a>')
#
#        # 3) Guardar
#        VehiculoVendido.objects.create(
#            vehiculo=vehiculo_obj,
#            fecha_venta=fecha_venta,
#            precio_venta=precio,
#            comprador=comprador,
#        )
#        mensaje = '<h2>Venta guardada</h2><br><a href="/">Inicio</a>'
#    else:
#        mensaje = '<h2>Debe ingresar todos los campos de la venta</h2><br><a href="/">Inicio</a>'
#
#    return HttpResponse(mensaje)




@requiere_sesion
def ingresarVehiculoVendido(request):
    vehiculo_id = request.GET.get("txt_id_vehiculo", "").strip()
    fecha_venta = request.GET.get("txt_fecha_venta", "").strip()
    precio_venta = request.GET.get("txt_precio_venta", "").strip()
    comprador = request.GET.get("txt_comprador", "").strip()

    # --- Validación de precio con dos decimales ---
    try:
        precio = Decimal(precio_venta)
        dos_decimales = precio == precio.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        dos_decimales = False

    # --- Validación de campos y longitudes ---
    if (not vehiculo_id or not fecha_venta or not precio_venta or not comprador
            or len(precio_venta) > 10
            or len(comprador) > 150
            or not dos_decimales):
        mensaje = "Debe ingresar todos los campos de la venta respetando sus longitudes y formato."
        tipo_mensaje = "error"
        return render(request, "automotora/resultado_operacion_vendido.html", {
            "mensaje": mensaje,
            "tipo_mensaje": tipo_mensaje,
        })

    # --- Verificar vehículo y guardar de forma atómica ---
    try:
        with transaction.atomic():
            vehiculo_obj = Vehiculo.objects.get(id_vehiculo=vehiculo_id)

            if VehiculoVendido.objects.filter(vehiculo=vehiculo_obj).exists():
                raise ValueError("vehiculo_ya_vendido")

            VehiculoVendido.objects.create(
                vehiculo=vehiculo_obj,
                fecha_venta=fecha_venta,
                precio_venta=precio,
                comprador=comprador,
            )
    except Vehiculo.DoesNotExist:
        mensaje = "El vehículo indicado no existe."
        tipo_mensaje = "error"
    except ValueError as e:
        if str(e) == "vehiculo_ya_vendido":
            mensaje = "Ese vehículo ya fue vendido."
        else:
            mensaje = "Los datos de la venta no son válidos."
        tipo_mensaje = "error"
    except IntegrityError:
        mensaje = "No fue posible registrar la venta. Verifique los datos ingresados."
        tipo_mensaje = "error"
    else:
        mensaje = "Venta guardada correctamente."
        tipo_mensaje = "success"

    return render(request, "automotora/resultado_operacion_vendido.html", {
        "mensaje": mensaje,
        "tipo_mensaje": tipo_mensaje,
    })

























@requiere_sesion
def listarClientes(request):
    clientes = Cliente.objects.all()
    vehiculos = Vehiculo.objects.all()
    return render(request,
                  'automotora/listar_clientes_vehiculos.html',{'clientes':clientes,
                                                               'vehiculos':vehiculos})

@requiere_sesion
def listarVendidos(request):
    vendidos = VehiculoVendido.objects.all()
    vehiculos = Vehiculo.objects.all()
    return render(request,
                  'automotora/listar_vehiculos.vendidos.html',{'vendidos':vendidos,
                                                               'vehiculos':vehiculos})

@requiere_sesion
def buscar(request):
    if request.GET["txt_rut"]:
        rut=request.GET["txt_rut"]
        cliente=Cliente.objects.filter(rut__icontains=rut)
        return render(request,
                      "automotora/busqueda_cliente.html",{"clientes":cliente,
                                                          "busqueda_realizada":True})
    else:
        mensaje='<h2>Debe ingresar un RUT de cliente</h2><br><a href="/">Inicio</a>'
        return HttpResponse(mensaje)

@requiere_sesion
def listarBorrar(request):
    vehiculos = Vehiculo.objects.all()
    clientes = Cliente.objects.all()
    return render(request,
                  'automotora/eliminar_vehiculo_cliente.html',{"vehiculos":vehiculos,
                                                               "clientes":clientes})

@requiere_sesion
@require_POST
def eliminar_vehiculo(request):
    id_recibido = request.POST.get("txt_id_vehiculo", "").strip()

    if not id_recibido:
        return HttpResponse('<h2>Error: no se recibió el ID</h2><br><a href="/">Inicio</a>')

    try:
        vehiculo = Vehiculo.objects.get(id_vehiculo=id_recibido)
        vehiculo.delete()
        mensaje = '<h2>Vehículo eliminado</h2><br><a href="/">Inicio</a>'
    except Vehiculo.DoesNotExist:
        mensaje = '<h2>Vehículo no encontrado</h2><br><a href="/">Inicio</a>'

    return HttpResponse(mensaje)


def validarLogin(request):
    if request.method != 'POST':
        return redirect('login')

    username = request.POST.get('txt_usuario', '').strip()
    password = request.POST.get('txt_password', '')

    if not username or not password:
        return render(request, 'automotora/login.html', {'error': 'Debe completar ambos campos'})

    try:
        usuario = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
        return render(request, 'automotora/login.html', {'error': 'Usuario o contraseña incorrectos'})

    if not usuario.check_password(password):
        return render(request, 'automotora/login.html', {'error': 'Usuario o contraseña incorrectos'})

    request.session['usuario_id'] = usuario.id_usuario
    request.session['usuario_username'] = usuario.username

    return redirect('home_page')


@requiere_sesion
@require_POST
def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')