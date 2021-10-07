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
from account.views import (registration_form, logout_view, login_view)
from wyniki.views import (wyniki_edycja,  wyniki, rejestracja_na_zawody, wyniki_edit, exportexcel)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
    path('register/', registration_form, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('wyniki_edycja/', wyniki_edycja, name="wyniki_edycja"),
    path('wyniki/', wyniki, name="wyniki"),
    # path('savestudent/', savestudent, name="savestudent"),
    path('rejestracja_na_zawody/', rejestracja_na_zawody, name="rejestracja_na_zawody"),
    # path('wyniki_edit/', wyniki_edit, name="wyniki_edit"),
    # url(r'^(?P<slug>[-\w]+)/$', wyniki_edit, name="wyniki_edit"),
    url(r'^(?P<slug>[-\w]+)/'r'(?P<nr_zawodow>[-\w]+)/$', wyniki_edit, name="wyniki_edit"),
    path('exportexcel', exportexcel, name="exportexcel"),
]
