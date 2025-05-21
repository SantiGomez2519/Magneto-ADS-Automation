from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ad.models import Campaign
from user_segmentation.models import UserProfile, CampaignSegment

@login_required(login_url='login')
def home(request):
    total_campaigns = Campaign.objects.count()
    total_users = UserProfile.objects.count()
    total_segments = CampaignSegment.objects.count()
    total_conversions = CampaignSegment.objects.filter(conversion_actual=True).count()
    recent_campaigns = Campaign.objects.all().order_by('-id')[:5]
    return render(request, "home.html", {
        'total_campaigns': total_campaigns,
        'total_users': total_users,
        'total_segments': total_segments,
        'total_conversions': total_conversions,
        'recent_campaigns': recent_campaigns,
    })