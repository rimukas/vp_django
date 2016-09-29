"""vp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from vart import views
#from vart.views import HomePageView
#from vart.views import SignUpView
#from vart.views import LoginView
#from vart.views import LogOutView
#from vart.views import PlanasView
#from vart.views import KodasView
#from vart.views import Planas


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', views.HomePageView.as_view(), name='home'),
    url('^home/', views.HomePageView.as_view(), name='home'),
    url(r'^accounts/register/$', views.SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.LogOutView.as_view(), name='logout'),
    url(r'^planas/$', views.PlanasView, name='planas'),
    url(r'^planas/([0-9-]+)$', views.KodasView, name='planas'),
   # url(r'^planas/kodas_add$', views.PlanasAdd.as_view(), name='planas_add'),
    url(r'^planas/kodas_add$', views.PlanasAdd.as_view(), name='planas_add'),
]
