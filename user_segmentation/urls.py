from django.urls import path
from . import views

app_name = 'user_segmentation'

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('campaign/<int:campaign_id>/segment/', views.segment_campaign, name='segment_campaign'),
    path('campaign/<int:campaign_id>/metrics/', views.campaign_metrics, name='campaign_metrics'),
    path('dashboard/', views.dashboard, name='dashboard'),
] 