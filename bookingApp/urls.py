from django.urls import include, path
from . import views

urlpatterns = [

    path("", views.homePage, name="homepage"),
    path("calendar",views.calendar,name="calendar")
    ]