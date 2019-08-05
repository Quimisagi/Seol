from django.db import models
from apps.usuarios.models import  Usuario
from apps.productos.models import Producto
# Create your models here.

class Factura (models.Model):
    idFactura = models.IntegerField(primary_key=True)
    usuario=models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE )
    fechayHora = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    estado = models.BooleanField()



class FacturaPorProducto (models.Model):
    idFacturaPorProducto = models.IntegerField(primary_key=True)
    factura = models.ForeignKey(Factura, null=True, blank=True, on_delete=models.CASCADE )
    producto = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.CASCADE )
    precioVenta = models.FloatField()
    descuento =  models.IntegerField()
    IVA =  models.IntegerField()
    cantidad = models.IntegerField()
    subtotal = models.IntegerField()

