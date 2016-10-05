from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

'''
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
'''


class Planas(models.Model):
    PDP = (
        ('paslauga', 'Paslauga'),
        ('darbas', 'Darbas'),
        ('preke', 'Prekė'))
    organizatorius = models.ForeignKey(
        User,
        to_field='username',
        on_delete=models.CASCADE
        )
    kodas = models.CharField(max_length=30, unique=True)
    preke = models.CharField(
        max_length=100,
        verbose_name='Prekė, paslauga, darbas',
        unique=True
        )
    islaidos = models.DecimalField(max_digits=9, decimal_places=2)
    paslauga_darbas_preke = models.CharField(
        max_length=8,
        default='preke',
        choices=PDP
        )

    class Meta:
        verbose_name = "Planas"
        verbose_name_plural = "Planas"
        ordering = ['kodas']

    def __str__(self):
        return self.kodas + ': ' + self.preke


class Sutartis(models.Model):
    kodas = models.ForeignKey(
        Planas, to_field='kodas',
        on_delete=models.SET_NULL,
        verbose_name='Kodas',
        null=True
        )
    '''
    preke_sut = models.ForeignKey(
        Planas,
        to_field='preke',
        on_delete=models.SET_NULL,
        related_name='preke_sut',
        verbose_name='Pavadinimas',
        null=True
        )
    '''
    data = models.DateField(default=date.today, verbose_name='Sutarties data')
    suma = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Planuojama Suma'
        )
    tiekejo_kodas = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        verbose_name='Tiekėjo kodas'
        )
    tiekejas = models.CharField(max_length=100, verbose_name='Tiekėjas')
    pastaba = models.CharField(
        max_length=200,
        verbose_name='Pastaba',
        blank=True
        )
    zalias = models.BooleanField(
        default=False,
        verbose_name='Ar tai žalias pirkimas?'
        )

    class Meta:
        verbose_name = "Sutartis"
        verbose_name_plural = "Sutartis"

    def __str__(self):
        return self.tiekejas

