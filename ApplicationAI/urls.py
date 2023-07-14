from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name = "index"),
        path("download", views.download, name = "download"),
        path("app", views.app, name = "app"),
        path("register", views.register, name = "register"),
        path("login", views.login_view, name = "login"),
        path("getJsonData", views.getJsonData, name = "getJsonData")
        ]
