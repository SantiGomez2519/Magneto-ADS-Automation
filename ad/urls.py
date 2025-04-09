from django.urls import path
from .views import create_campaign, campaign_list, campaign_success, schedule_ad

urlpatterns = [
    path("create/", create_campaign, name="create_campaign"),
    path("campaigns/", campaign_list, name="campaign_list"),
    path("success/",campaign_success, name="campaign_success"),
    path("schedule/", schedule_ad, name="schedule_ad")
]
