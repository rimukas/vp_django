from django.contrib import admin
from .models import Vartotojai, Planas

# Register your models here.


class PlanasAdmin(admin.ModelAdmin):
	# list_display = ('upper_case_name')
	list_filter = ('organizatorius',)


class VartotojaiAdmin(admin.ModelAdmin):
	list_display = ('organizatorius', 'pareigos', 'adminas', 'aktyvus')
	list_filter = ('aktyvus',)


admin.site.register(Vartotojai, VartotojaiAdmin)
admin.site.register(Planas, PlanasAdmin)