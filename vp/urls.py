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
#from vart.views import kodas_view
#from vart.views import Planas


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', views.HomePageView.as_view(), name='home'),
    url('^home/', views.HomePageView.as_view(), name='home'),
    url(r'^accounts/register/$', views.SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.LogOutView.as_view(), name='logout'),
    url(r'^planas/$', views.planas_view, name='planas'),
    url(r'^planas/(?P<kodas>\d+)/$', views.PlanasUpdate.as_view(), name='planas_update'),
    url(r'^planas/delete/(?P<kodas>\d+)/$', views.planas_delete_confirm, name='planas_delete_confirm'),
    url(r'^planas/delete/del/(?P<kodas>\d+)/$', views.planas_delete, name='planas_delete'),
    # url(r'^planas/delete/del/(?P<kodas>\d+)/$', views.PlanasDelete.as_view(), name='planas_delete'),
    # url(r'^planas/kodas_add$', views.PlanasAdd.as_view(), name='planas_add'),
    url(r'^planas/kodas_add$', views.PlanasAdd.as_view(), name='planas_add'),
    url(r'^mano_sutartis/(?P<kodas>[0-9-]+)/$', views.sutartis_view, name='sutartis_view'),
    url(r'^mano_sutartis/update/(?P<id_pk>[0-9-]+)/$', views.SutartisUpdate.as_view(), name='sutartis_update'),
    url(r'^mano_sutartis/copy/(?P<id_pk>[0-9-]+)/$', views.sutartis_copy, name='sutartis_copy'),
    url(r'^mano_sutartis/delete/(?P<id_pk>[0-9-]+)/$', views.sutartis_delete_confirm, name='sutartis_delete_confirm'),
    url(r'^mano_sutartis/delete/del/(?P<id_pk>[0-9-]+)/$', views.SutartisDelete.as_view(), name='sutartis_delete'),
    url(r'^mano_sutartis/sutartis_add/(?P<kodas>[0-9-]+)/$', views.SutartisAdd.as_view(), name='sutartis_add'),
    url(r'^laikotarpis/$', views.laikotarpis, name='laikotarpis'),
    # url(r'^mano_sutartis/copy/(?P<kodas>[0-9]+)/$', views.SutartisUpdate.as_view(), name='sutartis_update'),
]
