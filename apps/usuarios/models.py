from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

documentos=(('CC','cedula de ciudadania'),('TI','tarjeta de identidad'),('PA','pasaporte'),('CE','cedula de extranjeria'))

class Usuario(AbstractUser):
    nombres = models.CharField(max_length=45, null=False)
    apellidos = models.CharField(max_length=45, null=False)
    tipo_documento = models.CharField(max_length=20, null=False, choices=documentos)
    numero_documento = models.CharField(max_length=45, null=False, unique=True)
    telefono = models.CharField(max_length=45, null=True)
    direccion = models.CharField(max_length=45, null=True)
    fecha_nacimiento = models.DateField(null=True)
    estado = models.BooleanField(default=True)
    email = models.EmailField(('Correo'), unique=True, null=False)
    es_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    imagen = models.ImageField(default='default.jpg', upload_to='fotos_perfil')

    def __str__(self):
        return 'Perfil de ' + self.usuario.nombres

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.imagen.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.imagen.path)

     
@receiver(post_save, sender=Usuario)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=Usuario)
def guarda_perfil(sender, instance, **kwargs):
    instance.perfil.save()


