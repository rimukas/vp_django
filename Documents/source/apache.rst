Paleidimas per Apache serverį
-----------------------------

Toliau aprašomas pats paprasčiausias ir greičiausias būdas sistemos paleidimui per Apache serverį. Visų pirma, kompiuteryje jau turi būti įdiegtas Apache web serveris. Po to reikia instaliuoti mod_wsgi (https://github.com/GrahamDumpleton/mod_wsgi/tree/1abae882b904a39de6756f18a94363676208c3ff):
::

	pip install mod_wsgi


Django settings faile, INSTALLED_APPS turi būti pridėtas mod_wsgi.server:
::

	INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'mod_wsgi.server',
	)

Django settings.py faile, STATIC_ROOT kintamajame turi būti nurodyta static failų vieta (pvz. STATIC_ROOT = "/var/www/site"). Po to reikia surinkti static failus į nurodytą vietą. Paleidžiam komandą:
::

	python manage.py collectstatic

Dabar galima paleisti Apache serverį su mod_wsgi (portas 8000), per kurį bus pasiekiama Django aplikacija:
::

	python manage.py runmodwsgi

Daugiau mod_wsgi nustatymų ir galimybių čia: https://github.com/GrahamDumpleton/mod_wsgi/tree/1abae882b904a39de6756f18a94363676208c3ff


