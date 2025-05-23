from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ad.models import Campaign, PlatformMetrics
from user_segmentation.models import UserProfile, CampaignSegment
from django.db.models import Sum
import json
from datetime import datetime

@login_required(login_url='login')
def home(request):
    total_campaigns = Campaign.objects.count()
    total_users = UserProfile.objects.count()
    total_segments = CampaignSegment.objects.count()
    total_conversions = CampaignSegment.objects.filter(conversion_actual=True).count()
    recent_campaigns = Campaign.objects.all().order_by('-id')[:5]

    # KPIs y gráfico por plataforma
    platforms = [p[0] for p in Campaign.PLATFORM_CHOICES]
    platform_names = [p[1] for p in Campaign.PLATFORM_CHOICES]
    kpi_data = {}
    bar_data = {'labels': platform_names, 'impressions': [], 'clicks': [], 'conversions': []}
    for code, name in Campaign.PLATFORM_CHOICES:
        metrics = PlatformMetrics.objects.filter(platform=code)
        impressions = metrics.aggregate(total=Sum('impressions'))['total'] or 0
        clicks = metrics.aggregate(total=Sum('clicks'))['total'] or 0
        conversions = metrics.aggregate(total=Sum('conversions'))['total'] or 0
        kpi_data[code] = {
            'name': name,
            'impressions': impressions,
            'clicks': clicks,
            'conversions': conversions,
        }
        bar_data['impressions'].append(impressions)
        bar_data['clicks'].append(clicks)
        bar_data['conversions'].append(conversions)

    context = {
        'total_campaigns': total_campaigns,
        'total_users': total_users,
        'total_segments': total_segments,
        'total_conversions': total_conversions,
        'recent_campaigns': recent_campaigns,
        'kpi_data': kpi_data,
        'bar_labels': json.dumps(bar_data['labels']),
        'bar_impressions': json.dumps(bar_data['impressions']),
        'bar_clicks': json.dumps(bar_data['clicks']),
        'bar_conversions': json.dumps(bar_data['conversions']),
    }
    return render(request, "home.html", context)