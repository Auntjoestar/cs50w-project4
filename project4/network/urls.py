
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watch_profile", views.watch_profile, name="watch_profile"),
    path("watch_profile_picture", views.watch_profile_picture, name="watch_profile_picture"),
    path("set_profile", views.set_profile, name="set_profile"),
    path("change_picture", views.change_picture, name="change_picture")
]
