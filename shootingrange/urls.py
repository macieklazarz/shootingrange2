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
from account.views import (registration_form, registration_form_no_login, logout_view, login_view, AccountListView, AccountUpdateView, AccountDeleteView, PasswordResetViewNew, PasswordResetDoneViewNew, PasswordResetConfirmViewNew, PasswordResetCompleteViewNew)
from wyniki.views import (wyniki_edycja,  wyniki, rejestracja_na_zawody,  exportexcel, WynikUpdateView, not_authorized, RejestracjaNaZawodyView, KonkurencjaDeleteView, TurniejListView, TurniejDeleteView, TurniejEditView, TurniejCreateView, OplataListView, OplataUpdateView, UczestnikDeleteView)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home_screen_view, name="home"),
    path('<int:pk>/', home_screen_view, name="home"),
    path('<int:pk>/register/', registration_form, name="register"),
    path('register_no_login/', registration_form_no_login, name="register_no_login"),
    # path('users/', AccountListView.as_view(), name="users"),
    path('users/<int:pk>/', AccountListView.as_view(), name="users"),
    # path('users_rts/', RtsListView.as_view(), name="users_rts"),
    path('logout/<int:pk>', logout_view, name="logout"),
    path('login/<int:pk>/', login_view, name="login"),
    path('<int:pk>/wyniki_edycja/', wyniki_edycja, name="wyniki_edycja"),
    # path('wyniki/', wyniki, name="wyniki"),
    path('wyniki/<int:pk>/', wyniki, name="wyniki"),
    # path('savestudent/', savestudent, name="savestudent"),
    # path('rejestracja_na_zawody/', rejestracja_na_zawody, name="rejestracja_na_zawody"),
    # path('rejestracja_na_zawody/', RejestracjaNaZawodyView.as_view(), name="rejestracja_na_zawody"),
    path('rejestracja_na_zawody/<int:pk>/', RejestracjaNaZawodyView.as_view(), name="rejestracja_na_zawody"),
    # path('wyniki_edit/', wyniki_edit, name="wyniki_edit"),
    # url(r'^(?P<slug>[-\w]+)/$', wyniki_edit, name="wyniki_edit"),
    # url(r'^(?P<slug>[-\w]+)/'r'(?P<nr_zawodow>[-\w]+)/$', wyniki_edit, name="wyniki_edit"),
    path('<int:pk>/wyniki_edit/<int:pk_turniej>/', WynikUpdateView.as_view(), name="wyniki_edit"),
    path('<int:pk>/account_edit/<int:pk_turniej>/', AccountUpdateView.as_view(), name="account_edit"),
    path('<int:pk>/account_delete/<int:pk_turniej>/',AccountDeleteView.as_view(), name="account_delete"),
    # path('<int:pk>/rts_delete/',RtsDeleteView.as_view(), name="rts_delete"),
    # path('<int:pk>/konkurencja_delete/',KonkurencjaDeleteView.as_view(), name="konkurencja_delete"),
    path('<int:pk>/konkurencja_delete/<int:pk_turniej>',KonkurencjaDeleteView.as_view(), name="konkurencja_delete"),
    # path('<int:pk>/konkurencja_delete/<int:pk_konkurencja>/',KonkurencjaDeleteView.as_view(), name="konkurencja_delete"),
    path('<int:pk>/exportexcel', exportexcel, name="exportexcel"),
    # path('dodaj_zawody/', ZawodyCreateView.as_view(), name="dodaj_zawody"),
    path('dodaj_zawody/<int:pk>/', ZawodyCreateView.as_view(), name="dodaj_zawody"),
    path('<int:pk>/dodaj_sedziego/', SedziaCreateView.as_view(), name="dodaj_sedziego"),
    path('<int:pk>/sedzia_lista/', SedziaListView.as_view(), name="sedzia_lista"),
    # path('zawody_lista', ZawodyListView.as_view(), name="zawody_lista"),
    path('zawody_lista/<int:pk>', ZawodyListView.as_view(), name="zawody_lista"),
    # path('<int:pk>/zawody_delete/', ZawodyDeleteView.as_view(), name="zawody_delete"),
    path('<int:pk>/zawody_delete/<int:pk_turniej>', ZawodyDeleteView.as_view(), name="zawody_delete"),
    path('<int:pk>/delete/<int:pk_turniej>',SedziaDeleteView.as_view(), name="sedzia_delete"),
    path('not_authorized/',not_authorized, name="not_authorized"),
    path('<int:pk>/turnieje/',TurniejListView.as_view(), name="turnieje"),
    path('<int:pk>/turniej_edit/<int:pk_turniej>/', TurniejEditView.as_view(), name="turniej_edit"),
    path('<int:pk>/turniej_delete/<int:pk_turniej>/', TurniejDeleteView.as_view(), name="turniej_delete"),
    path('<int:pk>/turniej_add/', TurniejCreateView.as_view(), name="turniej_add"),
    path('oplata/<int:pk>/', OplataListView.as_view(), name="oplata_list"),
    path('<int:pk>/oplata_update/<int:pk_turniej>/', OplataUpdateView.as_view(), name="oplata_update"),
    # path('/rts_add/', RtsCreateView.as_view(), name="rts_add"),
    path('<int:pk>/uczestnik_delete/<int:pk_turniej>/',UczestnikDeleteView.as_view(), name="uczestnik_delete"),


    path('<int:pk>/password_reset/',
        PasswordResetViewNew.as_view(),
        name="password_reset"),
    path('<int:pk>/password_reset/done/',
        PasswordResetDoneViewNew.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        PasswordResetConfirmViewNew.as_view(),
        name='password_reset_confirm'),
    path('/reset/done/',
        PasswordResetCompleteViewNew.as_view(),
        name='password_reset_complete'),
]
