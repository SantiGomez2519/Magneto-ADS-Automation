from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path("", home, name="home"),
    path('', views.interaction_dashboard, name='dashboard'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('report/', views.report_view, name='report'),
]
