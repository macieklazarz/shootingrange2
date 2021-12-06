"""shootingrange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from mainapp.views import (home_screen_view,)
from zawody.views import (ZawodyCreateView,SedziaCreateView, SedziaListView, SedziaDeleteView, ZawodyListView, ZawodyDeleteView )
from account.views import (registration_form, registration_form_no_login, logout_view, login_view, AccountListView, AccountUpdateView, AccountDeleteView)
from wyniki.views import (wyniki_edycja,  wyniki, rejestracja_na_zawody,  exportexcel, WynikUpdateView, not_authorized, RejestracjaNaZawodyView, KonkurencjaDeleteView, UstawieniaListView, UstawieniaUpdateView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
    path('register/', registration_form, name="register"),
    path('register_no_login/', registration_form_no_login, name="register_no_login"),
    path('users/', AccountListView.as_view(), name="users"),
    # path('users_rts/', RtsListView.as_view(), name="users_rts"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('wyniki_edycja/', wyniki_edycja, name="wyniki_edycja"),
    path('wyniki/', wyniki, name="wyniki"),
    # path('savestudent/', savestudent, name="savestudent"),
    # path('rejestracja_na_zawody/', rejestracja_na_zawody, name="rejestracja_na_zawody"),
    path('rejestracja_na_zawody/', RejestracjaNaZawodyView.as_view(), name="rejestracja_na_zawody"),
    # path('wyniki_edit/', wyniki_edit, name="wyniki_edit"),
    # url(r'^(?P<slug>[-\w]+)/$', wyniki_edit, name="wyniki_edit"),
    # url(r'^(?P<slug>[-\w]+)/'r'(?P<nr_zawodow>[-\w]+)/$', wyniki_edit, name="wyniki_edit"),
    path('<int:pk>/wyniki_edit/', WynikUpdateView.as_view(), name="wyniki_edit"),
    path('<int:pk>/account_edit/', AccountUpdateView.as_view(), name="account_edit"),
    path('<int:pk>/account_delete/',AccountDeleteView.as_view(), name="account_delete"),
    # path('<int:pk>/rts_delete/',RtsDeleteView.as_view(), name="rts_delete"),
    path('<int:pk>/konkurencja_delete/',KonkurencjaDeleteView.as_view(), name="konkurencja_delete"),
    path('exportexcel', exportexcel, name="exportexcel"),
    path('dodaj_zawody', ZawodyCreateView.as_view(), name="dodaj_zawody"),
    path('dodaj_sedziego', SedziaCreateView.as_view(), name="dodaj_sedziego"),
    path('sedzia_lista', SedziaListView.as_view(), name="sedzia_lista"),
    path('zawody_lista', ZawodyListView.as_view(), name="zawody_lista"),
    path('<int:pk>/zawody_delete/', ZawodyDeleteView.as_view(), name="zawody_delete"),
    path('<int:pk>/delete/',SedziaDeleteView.as_view(), name="sedzia_delete"),
    path('not_authorized/',not_authorized, name="not_authorized"),
    path('ustawienia/',UstawieniaListView.as_view(), name="ustawienia"),
    path('<int:pk>/ustawienia_edit/', UstawieniaUpdateView.as_view(), name="ustawienia_update"),
    # path('/rts_add/', RtsCreateView.as_view(), name="rts_add"),
]
