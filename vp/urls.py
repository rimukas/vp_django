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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from vart import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', views.HomePageView.as_view(), name='home'),
    # register nenaudojamas, vartotojus prie sistemos turi prideti administratorius
    # url(r'^accounts/register/$', views.SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.LogOutView.as_view(), name='logout'),
    url(r'^laikotarpis/$', views.laikotarpis, name='laikotarpis'),
]

# planas
urlpatterns += [
    url(r'^planas/$', views.PlanasView.as_view(), name='planas'),
    url(r'^planas/(?P<kodas>\d+)/$', views.PlanasUpdate.as_view(), name='planas_update'),
    url(r'^planas/delete/(?P<kodas>\d+)/$', views.planas_delete_confirm, name='planas_delete_confirm'),
    url(r'^planas/delete/del/(?P<kodas>\d+)/$', views.PlanasDelete.as_view(), name='planas_delete'),
    # url(r'^planas/delete/del/(?P<kodas>\d+)/$', views.PlanasDelete.as_view(), name='planas_delete'),
    # url(r'^planas/kodas_add$', views.PlanasAdd.as_view(), name='planas_add'),
    url(r'^planas/kodas_add$', views.PlanasAdd.as_view(), name='planas_add'),
]

# sutartis
urlpatterns += [
    url(r'^mano_sutartis/(?P<kodas>[0-9-]+)/$', views.sutartis_view, name='sutartis_view'),
    url(r'^mano_sutartis/update/(?P<id_pk>[0-9-]+)/$', views.SutartisUpdate.as_view(), name='sutartis_update'),
    url(r'^mano_sutartis/copy/(?P<id_pk>[0-9-]+)/$', views.sutartis_copy, name='sutartis_copy'),
    url(r'^mano_sutartis/delete/(?P<id_pk>[0-9-]+)/$', views.sutartis_delete_confirm, name='sutartis_delete_confirm'),
    url(r'^mano_sutartis/delete/del/(?P<id_pk>[0-9-]+)/$', views.SutartisDelete.as_view(), name='sutartis_delete'),
    url(r'^mano_sutartis/sutartis_add/(?P<kodas>[0-9-]+)/$', views.SutartisAdd.as_view(), name='sutartis_add'),
]

# saskaitos fakturos
urlpatterns += [
    url(r'^faktura/(?P<id_pk>[0-9-]+)/$', views.FakturaView.as_view(), name='faktura'),
    url(r'^faktura/add/(?P<id_pk>[0-9-]+)/$', views.FakturaAdd.as_view(), name='faktura_add'),
    url(r'^faktura/update/(?P<id_pk>[0-9-]+)/$', views.FakturaUpdate.as_view(), name='faktura_update'),
    url(r'^faktura/copy/(?P<id_pk>[0-9-]+)/$', views.FakturaUpdate.as_view(), name='faktura_copy'),
    url(r'^faktura/delete/(?P<id_pk>[0-9-]+)/$', views.FakturaUpdate.as_view(), name='faktura_delete_confirm'),
    url(r'^faktura/delete/del/(?P<id_pk>[0-9-]+)/$', views.FakturaUpdate.as_view(), name='faktura_delete'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
