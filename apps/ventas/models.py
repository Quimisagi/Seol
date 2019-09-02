from django.db import models
from apps.productos.models import Producto
from apps.usuarios.models import Usuario

metodos=(('Efectivo','Dinero en efectivo'),('TC','Tarjeta Crédito'),('TD','Tarjeta Débito'))
franquicias=(('Mastercard','Mastercard'),('Visa','Visa'),('American','American Express'),('Diners','Diners club'))
bancos=(('Bancolombia','Bancolombia'),('BBVA','BBVA'),('Caja social','Caja social'),('Banco de Bogotá','Banco de Bogotá'))


class Factura(models.Model):
    #usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    id_usuario = models.IntegerField(null=True)
    nombre_usuario = models.CharField(max_length=30, null=True)
    apellido_usuario = models.CharField(max_length=30, null=True)
    direccion_usuario = models.CharField(max_length=30, null=True)
    telefono_usuario = models.CharField(max_length=30, null=True)
    ciudad_usuario = models.CharField(max_length=30, null=True)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(decimal_places=1, max_digits=100)
    estado = models.BooleanField(default=False)

class Factura_Producto(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(decimal_places=1, max_digits=100, null=True)

class Factura_Pago(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=20, null=False, choices=metodos)
    valor = models.DecimalField(decimal_places=1, max_digits=100)
    

class TarjetaD(models.Model):
    factura_pago = models.ManyToManyField(Factura_Pago)
    numero = models.IntegerField()
    fecha = models.CharField(max_length=30)
    banco = models.CharField(max_length=30, choices=bancos, null=True)

class TarjetaC(models.Model):
    factura_pago = models.ManyToManyField(Factura_Pago)
    numero = models.IntegerField()
    fecha = models.CharField(max_length=30)
    franquicia = models.CharField(max_length=30, choices=franquicias)
    cvv = models.IntegerField()
    cuotas = models.IntegerField()

#Factura(nombre_usuario='Cristina', apellido_usuario='Mejia', direccion_usuario='Calle 123', telefono_usuario='320214578', ciudad_usuario='Cali', total=2000, estado=True)



