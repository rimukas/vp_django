from django.db import models
from django.contrib.auth.models import User
from datetime import date
from model_utils.models import SoftDeletableModel


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


class Planas(SoftDeletableModel):
    """ Planas

    Paveldi klase SoftDeletableModel kartu su Manager'iu SoftDeletableManager.
    Reikalinga tam, kad netrintu jau ivesto plano is duombazes, kad reikalui esant
    ta plana butu galima atstatyti tam paciam ar kitam vartotoji.
    SoftDeletableModel netrina iraso, o tik ji pazymi is_deleted.
    """
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

    # deafaultinis Manager'is, grazina visus irasus, tame tarpe ir "istrintus"
    include_deleted = models.Manager()

    class Meta:
        verbose_name = "Planas"
        verbose_name_plural = "Planas"
        ordering = ['kodas']

    def __str__(self):
        return self.kodas + ': ' + self.preke


class Sutartis(models.Model):
    kodas = models.ForeignKey(
        Planas, to_field='kodas',
        on_delete=models.CASCADE,
        verbose_name='Kodas'
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
        k = self.kodas.kodas
        return 'ID:' + str(self.id)\
               + ', KODAS: ' + self.kodas.kodas\
               + ', PREKE: ' + self.kodas.preke\
               + ', DATA: ' + self.data.strftime('%Y-%m-%d')\
               + ', TIEKEJAS: ' + self.tiekejas


class Sf(models.Model):
    sf = models.CharField(max_length=50, verbose_name='Sąskaitos faktūros Nr.')
    sutartisid = models.ForeignKey(Sutartis, on_delete=models.CASCADE)
    suma = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Sąsk. faktūros suma'
        )
    data = models.DateField(verbose_name='Sąsk. faktūros data')
    pavadinimas = models.CharField(max_length=255, verbose_name='Pirkimo objektas')

    def __str__(self):
        return 'SUTARTIS: ' + self.sutartisid.kodas.kodas + ': ' + self.sutartisid.kodas.preke\
               + ', S.F.: ' + self.sf\
               + ', PAVADINIMAS: ' + self.pavadinimas\
               + ', S.F. SUMA: ' + str(self.suma)\
               + ', SUTARTIES DATA/S.F. DATA: ' + str(self.sutartisid.data) + '/' + str(self.data)

    class Meta:
        verbose_name = "Sąskaitos faktūros"
        verbose_name_plural = "Sąskaitos faktūros"
        ordering = ['data']
