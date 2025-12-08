from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('portal/', views.portal_view, name='portal'),
    path('calculator/', views.calculator_view, name='calculator'),
    path('clear-history/', views.clear_history, name='clear_history'),
    path('log-table/', views.show_log_table, name='log_table'),
    path('log-pdf/', views.generate_log_pdf, name='log_pdf'),
    path('settings/', views.settings_view, name='settings'),
]