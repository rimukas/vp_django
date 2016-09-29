from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Vartotojai(models.Model):
    organizatorius = models.CharField(max_length=50, unique=True)
    pareigos = models.CharField(max_length=200)
    adminas = models.BooleanField(default=False)
    aktyvus = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vartotojai"
        verbose_name_plural = "Vartotojai"

    def __str__(self):
        return self.organizatorius


class Planas(models.Model):
    PDP = (('paslauga', 'Paslauga'),
        ('darbas', 'Darbas'),
        ('preke', 'Prekė'))
    organizatorius = models.ForeignKey(User,
            to_field='username',
            on_delete=models.CASCADE)
    kodas = models.CharField(max_length=30)
    preke = models.CharField(max_length=100, verbose_name='Prekė, paslauga, darbas')
    islaidos = models.DecimalField(max_digits=9, decimal_places=2)
    paslauga_darbas_preke = models.CharField(max_length=8,
        default='preke',
        choices=PDP)

    class Meta:
        verbose_name = "Planas"
        verbose_name_plural = "Planas"

    def __str__(self):
        return self.preke
