from django.urls import path
from . import views

urlpatterns = [
    # La página de inicio ahora es la calculadora
    path('', views.calculator_view, name='calculator'),
    # Mantenemos la tabla de logaritmos en una ruta separada
    path('log-table/', views.show_log_table, name='log_table'),
    # Nueva ruta para generar el PDF de la tabla de logaritmos
    path('log-table/pdf/', views.generate_log_pdf, name='log_table_pdf'),
    path('calculadora/', views.calculator_view, name='calculator'),
]
