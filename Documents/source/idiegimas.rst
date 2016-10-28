Kompiuterio paruošimas ir sistemos įdiegimas
--------------------------------------------

Toliau bus aprašomas sistemos įdiegimas darbui lokaliame tinkle. Čia kaip pavyzdys bus naudojama Linux Ubuntu Server, nors tinka bet kokia Linux, MacOS ar Windows operacinė sistema, fizinė ar virtuali. 

Diegimas susideda iš šių etapų:
	
	* **Python 3.5+**;
	* **pip**;
	* **git**. 
	* **PostgreSQL**
	* **virtualenv**
	* **git repositoriumo klonavimas iš GitHub**
	* **pip reikalavimų instaliavimas iš requirements.txt**

Toliau aprašomas visas procesas smulkiau. Aišku, jei kompiuteryje jau yra kai kurie komponentai, tai tuos žingsnius galima praleisti. Taip pat nepamirštam, kad viską galima daryti *copy-paste* į terminalo langą ;)


1. Atnaujinam indeksus:
::

	sudo apt-get update


2. Instaliuojam python3:
:: 

	sudo apt-get install python3


3. Instaliuojam pip:
::

	sudo apt-get install python3-pip
	pip3 --upgrade pip


4. Instaliuojam git:
::

	sudo apt-get install git


5. Instaliuojam PostgreSQL:
::

	sudo apt-get install postgresql postgresql-contrib


6. Nebūtina, bet šios bibliotekos naudojamos Pillow duombazės struktūros įrasymui į paveiksliuką:
::

	sudo apt-get install libjpeg8-dev zlib1g-dev


7. Instaliuojam PostgreSQL - Python reikalavimus:
::

	sudo apt-get install python-psycorg2
	sudo apt-get install libpq-dev


8. Instaliuojam pitono virtualią aplinką:
::

	sudo apt-get install python3-virtualenv


9. Sukuriam virtualios aplinkos katalogą:
::
	
	mkdir ~/.virtualenvs


10. Sukuriam virtualią aplinką:
::

	cd ~/.virtualenvs/
	virtualenv djangovp
	

11. Aktyvuojam virtualią aplinką:
::

	source djangovp/bin/activate


12. Sukuriam projektų katalogą ir klonuojam į jį git repositoriumą:
::

	mkdir ~/projects/
	cd ~/projects/
	git clone http://github.com/rimukas/vp_django.git vp
	cd vp/vp/


13. Dabar reikia patikrinti arba pakeisti duombazės vartotojo vardą ir slaptažodį:
::
	
	nano settings.py


14. Instaliuojam pip reikalavimus: 
::	

	cd ..
	pip install -r requirements.txt


15. Sukuriam duombazės vartotoją (čia *vpadmin*):
::

	sudo -u postgres createuser -P vpadmin


16. Sukuriam duombazę (čia *vp*, nurodoma settings.py faile) ir priskirim jai ką tik sukurtą vartotoją, kuris bus duombazės savininkas:
::
	
	sudo -u postgres createdb -O vpadmin vp

17. Atliekam duombazės migraciją:
::

	./manage.py migrate

18. Sukuriam Django svetainės administratorių:
::

	./manage.py createsuperuser


19. Jei viskas daroma virtualioje mašinoje, tai reikia pasižiūrėti jos IP adresą (turi būti nustatytas *bridge mode*):
::

	ifconfig | grep addr

20. Tarkim, adresas buvo 192.168.2.133. Tada:
::

	./manage.py runserver 192.168.2.133:8000

21. Toliau nueinam į *host* mašiną ir interneto naršyklės lange rašom:
::

	192.168.2.133:8000/admin


Turi atsiverti administravimo panelis.


22. Jei viskas daroma lokaliame kompiuteryje, tai žingsnius 19, 20, 21 galima praleisti. Tada reikia tiesiog įvykdyti komandą:
::

	./manage.py runserver

ir naršyklėje atsidaryti puslapį, kuris nurodytas įvykdžius aukščiau esančią komandą.


**Keletas būtiniausių PostgreSQL duombazės komandų:**

Prisijungti super administratoriaus vardu prie duombazės komandinio lango:
::

	sudo -u postgres psql

Rodyti visas duombazes (duombazės komandiniame lange):
::

	postgres=#\l


Rodyti roles:
::

	postgres=#\du

Jei pamiršom duombazės vartotojo slaptažodį arba šiaip jį norim pakeisti:
::

	postgres=#ALTER USER user_name WITH PASSWORD 'password';


Suteikti visas teises vartotojui į duombazę:
::

	postgres=#GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;


PostgreSQL serverio perkrovimas:
::

	sudo /etc/init.d/postgresql reload

	 
