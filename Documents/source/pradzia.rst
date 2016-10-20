Darbo pradžia
-------------

Įdiegus programą į serverį ir sukūrus PostgreSQL duomenų bazę, pirmiausiai reikia sukurti super administratorių, kuris pridės ir valdys kitus sistemos vartotojus. Tam yra atliekama komanda:

::

	python manage.py createsuperuser

Po to galima paleisti serverį:

::

	python manage.py runserver

Jungtis prie administavimo puslapio:

::

	http://localserver:8000/admin

ir pridėti kitus vartotojus.


