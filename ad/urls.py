from django.urls import path
from .views import create_campaign, campaign_list, campaign_success, add, edit_campaign, delete_campaign, platforms_list, ad_preview, simulate_metrics_view, performance_metrics_view, simulate_platform_metrics

urlpatterns = [
    path("create/", create_campaign, name="create_campaign"),
    path("campaigns/", campaign_list, name="campaign_list"),
    path("success/",campaign_success, name="campaign_success"),
    path('add/', add, name='add'),
    path('edit/<int:campaign_id>/', edit_campaign, name='edit_campaign'),
    path('delete/<int:campaign_id>/', delete_campaign, name='delete_campaign'),
    path('platforms/', platforms_list, name='platforms_list'),
    path('platforms/<int:campaign_id>/simulate/<str:platform>/', simulate_platform_metrics, name='simulate_platform_metrics'),
    path('preview/<int:campaign_id>/<str:platform>/', ad_preview, name='ad_preview'),
    path('simulate-metrics/<int:campaign_id>/', simulate_metrics_view, name='simulate_metrics'),
    path('performance-metrics/', performance_metrics_view, name='performance_metrics'),
]
