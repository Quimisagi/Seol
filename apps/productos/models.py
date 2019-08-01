from django.db import models
from django.urls import reverse
from PIL import Image


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True)

    estado = models.BooleanField(default = True)


class Subcategoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True)
    estado = models.BooleanField(default = True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    

class Producto(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.TextField()
    precio_venta = models.FloatField(null=False) 
    cantidad_disponible = models.IntegerField(null=False)
    marca = models.CharField(max_length=50, null=False)
    estado = models.BooleanField(default = True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to='product_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.imagen.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.imagen.path)


class Detalle(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    estado = models.BooleanField(default = True)


class Detalle_Producto(models.Model):
    peso = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    garantia = models.CharField(max_length=50)
    tamano = models.CharField(max_length=50)
    densidad = models.CharField(max_length=50)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)



class Descuento_Producto(models.Model):
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    porcentaje = models
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)










