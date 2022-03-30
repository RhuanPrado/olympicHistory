"""history URL Configuration

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
from posixpath import basename
from django.contrib import admin
from django.urls import path, include


from rest_framework import routers

from olympic.api import viewsets

route = routers.DefaultRouter()

route.register(r'person', viewsets.PersonViewSet, basename="Person")
route.register(r'team', viewsets.TeamViewSet, basename="Team")
route.register(r'nationality', viewsets.NationalityViewSet, basename="Nationality")
route.register(r'game', viewsets.GameViewSet, basename="Game")
route.register(r'participationgame', viewsets.ParticipationGameViewSet, basename="ParticipationGame")
route.register(r'uploadfile', viewsets.FileUploadViewSet, basename="UploadFile")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls))
]
