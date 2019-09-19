from django.db import models
from apps.usuarios.models import Usuario
from apps.productos.models import Producto
from django.dispatch import receiver
from django.db.models.signals import post_save

class Carrito_Compras(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class Carrito_Compras_Producto(models.Model):
    carrito = models.ForeignKey(Carrito_Compras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(null=False)
    subtotal = models.DecimalField(decimal_places=1, max_digits=100)

@receiver(post_save, sender=Usuario)
def crear_carrito(sender, instance, created, **kwargs):
    if created:
        Carrito_Compras.objects.create(usuario=instance)

@receiver(post_save, sender=Usuario)
def guarda_carrito(sender, instance, **kwargs):
    instance.carrito_compras.save()