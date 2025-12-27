from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experiencia_profesional/', views.experiencia, name='experiencia'),
    path('acreditaciones/', views.reconocimientos, name='reconocimientos'),
    path('formacion_realizada/', views.cursos, name='cursos'),
    path('produccion_academica_laboral/', views.productos, name='productos'),
    path('listado_venta/', views.venta_garage, name='venta_garage'),
]