from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.handleLogin, name = "handleLogin"),
    path('logout/', views.handleLogout, name = "handleLogout"),
]