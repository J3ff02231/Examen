from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    director = models.CharField(max_length=100)
    anio = models.IntegerField()
    destacada = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo