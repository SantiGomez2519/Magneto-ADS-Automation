from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Campaign, AdMetrics, PlatformMetrics
from django.db.models import Q, Sum
from django.core.exceptions import ValidationError
import random
from django.http import HttpResponse
import csv
from datetime import datetime
import json


# Create your views here.
def add(request):
    return render(request, "add.html")

def campaign_success (request):
    return render(request, "campaign_success.html")

def create_campaign(request):
    if request.method == "POST":
        name = request.POST.get("campaignName", "").strip()
        description = request.POST.get("campaignDescription", "").strip()
        image = request.FILES.get("campaignImage")
        schedule = request.POST.get("schedule", "").strip()
        end_schedule = request.POST.get("end_schedule", "").strip()
        if end_schedule == "":
            end_schedule = None

        category = request.POST.get("category", "").strip()
        education_level = request.POST.get("education_level", "").strip()
        modality = request.POST.get("modality", "").strip()
        location = request.POST.get("location", "").strip()
        experience = request.POST.get("experience", "").strip()

        # Get selected platforms as a list
        selected_platforms = request.POST.getlist("platforms")

        # Validations
        if not all([name, description, image, schedule, category, education_level, modality, location, experience]):
            messages.error(request, "All fields are required.")
            return render(request, "add.html")

        # Validate at least one platform is selected
        if not selected_platforms:
            messages.error(request, "Please select at least one platform.")
            return render(request, "add.html")

        # Initialize platform variables as None
        platform1 = None
        platform2 = None
        platform3 = None

        # Sort platforms to ensure consistent order
        if 'GOOGLE' in selected_platforms:
            platform1 = 'GOOGLE'
        if 'FACEBOOK' in selected_platforms:
            platform2 = 'FACEBOOK'
        if 'INSTAGRAM' in selected_platforms:
            platform3 = 'INSTAGRAM'

        try:
            campaign = Campaign.objects.create(
                name=name,
                description=description,
                image=image,
                schedule=schedule,
                end_schedule=end_schedule,
                category=category,
                education_level=education_level,
                modality=modality,
                location=location,
                experience=experience,
                platform1=platform1,
                platform2=platform2,
                platform3=platform3
            )
            return render(request, "campaign_success.html")
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, "add.html")

    return render(request, "add.html")

def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if request.method == 'POST':
        campaign.name = request.POST.get('name', campaign.name)
        campaign.description = request.POST.get('description', campaign.description)
        campaign.schedule = request.POST.get('schedule', campaign.schedule)
        end_schedule = request.POST.get('end_schedule')
        campaign.end_schedule = end_schedule if end_schedule else None
        campaign.category = request.POST.get('category', campaign.category)
        campaign.education_level = request.POST.get('education_level', campaign.education_level)
        campaign.modality = request.POST.get('modality', campaign.modality)
        campaign.location = request.POST.get('location', campaign.location)
        campaign.experience = request.POST.get('experience', campaign.experience)

        if request.FILES.get('image'):
            campaign.image = request.FILES.get('image')

        # Handle platform changes
        selected_platforms = request.POST.getlist('platforms')
        
        # Reset all platforms
        campaign.platform1 = None
        campaign.platform2 = None
        campaign.platform3 = None
        
        # Assign platforms in order
        if 'GOOGLE' in selected_platforms:
            campaign.platform1 = 'GOOGLE'
        if 'FACEBOOK' in selected_platforms:
            campaign.platform2 = 'FACEBOOK'
        if 'INSTAGRAM' in selected_platforms:
            campaign.platform3 = 'INSTAGRAM'

        try:
            campaign.save()
            messages.success(request, "Campaign updated successfully.")
            return redirect('campaign_list')
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'edit_campaign.html', {'campaign': campaign})

def campaign_list(request):
    query = request.GET.get("q")
    if query:
        campaigns = Campaign.objects.filter(name__icontains=query)
    else:
        campaigns = Campaign.objects.all()
    return render(request, "campaign_list.html", {"campaigns": campaigns})

def delete_campaign(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, id=campaign_id)
        campaign.delete()
    return redirect('campaign_list')

def platforms_list(request):
    query = request.GET.get('q', '')
    if query:
        campaigns = Campaign.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        campaigns = Campaign.objects.all()
    campaigns = campaigns.prefetch_related('platform_metrics')

    for campaign in campaigns:
        active_platforms = [p for p in [campaign.platform1, campaign.platform2, campaign.platform3] if p]
        n = len(active_platforms)
        if n == 0:
            continue
        # SIEMPRE sincronizar PlatformMetrics con AdMetrics
        # Buscar métricas totales existentes
        total_metrics = None
        if hasattr(campaign, 'metrics'):
            total_metrics = {
                'impressions': campaign.metrics.impressions,
                'clicks': campaign.metrics.clicks,
                'ctr': campaign.metrics.ctr,
                'conversions': campaign.metrics.conversions,
                'conversion_rate': campaign.metrics.conversion_rate,
                'cpc': campaign.metrics.cpc,
                'cpa': campaign.metrics.cpa,
                'spend': campaign.metrics.spend,
            }
        else:
            # Simular y crear AdMetrics
            total_metrics = simulate_campaign_metrics(campaign)
            AdMetrics.objects.create(campaign=campaign, **total_metrics)
        # Repartir aleatoriamente pero consistente
        def random_partition(total, parts):
            cuts = sorted([0] + [random.randint(0, total) for _ in range(parts-1)] + [total])
            return [cuts[i+1] - cuts[i] for i in range(parts)]
        def random_partition_float(total, parts):
            cuts = sorted([0] + [random.uniform(0, total) for _ in range(parts-1)] + [total])
            return [cuts[i+1] - cuts[i] for i in range(parts)]
        clicks_parts = random_partition(total_metrics['clicks'], n)
        impressions_parts = random_partition(total_metrics['impressions'], n)
        conversions_parts = random_partition(total_metrics['conversions'], n)
        spend_parts = random_partition_float(total_metrics['spend'], n)
        for i, plat in enumerate(active_platforms):
            clicks = clicks_parts[i]
            impressions = impressions_parts[i]
            conversions = conversions_parts[i]
            ctr = (clicks / impressions * 100) if impressions else 0
            conversion_rate = (conversions / clicks * 100) if clicks else 0
            cpc = (spend_parts[i] / clicks) if clicks else 0
            cpa = (spend_parts[i] / conversions) if conversions else 0
            PlatformMetrics.objects.update_or_create(
                campaign=campaign,
                platform=plat,
                defaults={
                    'impressions': impressions,
                    'clicks': clicks,
                    'ctr': ctr,
                    'conversions': conversions,
                    'conversion_rate': conversion_rate,
                    'cpc': cpc,
                    'cpa': cpa,
                    'spend': spend_parts[i],
                }
            )
    return render(request, 'platforms_list.html', {'campaigns': campaigns})

def ad_preview(request, campaign_id, platform):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    # Verificar que la plataforma solicitada está activa para esta campaña
    if platform == 'google' and not campaign.platform1:
        messages.error(request, 'Google platform not enabled for this campaign')
        return redirect('platforms_list')
    elif platform == 'facebook' and not campaign.platform2:
        messages.error(request, 'Facebook platform not enabled for this campaign')
        return redirect('platforms_list')
    elif platform == 'instagram' and not campaign.platform3:
        messages.error(request, 'Instagram platform not enabled for this campaign')
        return redirect('platforms_list')
    
    context = {
        'campaign': campaign,
        'platform': platform.upper(),
    }
    
    return render(request, 'ad_preview_page.html', context)

def simulate_campaign_metrics(campaign):
    # Simulación basada en la categoría y plataformas
    impressions = random.randint(2000, 20000)
    clicks = random.randint(int(impressions * 0.01), int(impressions * 0.15))
    ctr = (clicks / impressions) * 100 if impressions else 0
    conversions = random.randint(int(clicks * 0.05), max(1, int(clicks * 0.25)))
    conversion_rate = (conversions / clicks) * 100 if clicks else 0
    cpc = round(random.uniform(0.1, 2.0), 2)
    cpa = round(random.uniform(1.0, 10.0), 2)
    spend = round(clicks * cpc, 2)
    return {
        'impressions': impressions,
        'clicks': clicks,
        'ctr': ctr,
        'conversions': conversions,
        'conversion_rate': conversion_rate,
        'cpc': cpc,
        'cpa': cpa,
        'spend': spend,
    }

def simulate_metrics_view(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    # Si ya existen métricas, actualízalas; si no, créalas
    data = simulate_campaign_metrics(campaign)
    metrics, created = AdMetrics.objects.update_or_create(
        campaign=campaign,
        defaults=data
    )
    messages.success(request, 'Metrics simulated successfully!')
    # Redirigir al referer si existe, si no a performance_metrics
    next_url = request.META.get('HTTP_REFERER')
    if next_url and 'performance-metrics' in next_url:
        return redirect('performance_metrics')
    return redirect('campaign_list')

def performance_metrics_view(request):
    # Filtros
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    campaign_id = request.GET.get('campaign')
    platform = request.GET.get('platform')
    export = request.GET.get('export')

    # Query base
    metrics_qs = PlatformMetrics.objects.select_related('campaign')
    if start_date:
        metrics_qs = metrics_qs.filter(created_at__date__gte=start_date)
    if end_date:
        metrics_qs = metrics_qs.filter(created_at__date__lte=end_date)
    if campaign_id:
        metrics_qs = metrics_qs.filter(campaign__id=campaign_id)
    if platform:
        metrics_qs = metrics_qs.filter(platform=platform)

    # KPIs globales
    summary = metrics_qs.aggregate(
        total_impressions=Sum('impressions') or 0,
        total_clicks=Sum('clicks') or 0,
        total_conversions=Sum('conversions') or 0,
        total_spend=Sum('spend') or 0
    )
    summary['ctr'] = (summary['total_clicks'] / summary['total_impressions'] * 100) if summary['total_impressions'] else 0
    summary['conversion_rate'] = (summary['total_conversions'] / summary['total_clicks'] * 100) if summary['total_clicks'] else 0
    summary['cpc'] = (summary['total_spend'] / summary['total_clicks']) if summary['total_clicks'] else 0
    summary['cpa'] = (summary['total_spend'] / summary['total_conversions']) if summary['total_conversions'] else 0

    # Exportar a CSV
    if export == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="performance_metrics.csv"'
        writer = csv.writer(response)
        writer.writerow(['Campaign', 'Platform', 'Impressions', 'Clicks', 'CTR', 'Conversions', 'Conversion Rate', 'CPC', 'CPA', 'Spend', 'Date'])
        for m in metrics_qs:
            writer.writerow([
                m.campaign.name,
                m.get_platform_display(),
                m.impressions,
                m.clicks,
                f"{m.ctr:.2f}",
                m.conversions,
                f"{m.conversion_rate:.2f}",
                f"{m.cpc:.2f}",
                f"{m.cpa:.2f}",
                f"{m.spend:.2f}",
                m.created_at.strftime('%Y-%m-%d'),
            ])
        return response

    # Para filtros
    campaigns = Campaign.objects.all()
    platforms = Campaign.PLATFORM_CHOICES

    # Para gráfica de barras
    chart_labels = ['Impressions', 'Clicks', 'Conversions']
    chart_data = [summary['total_impressions'], summary['total_clicks'], summary['total_conversions']]

    context = {
        'metrics': metrics_qs,
        'summary': summary,
        'campaigns': campaigns,
        'platforms': platforms,
        'selected_campaign': int(campaign_id) if campaign_id else '',
        'selected_platform': platform or '',
        'start_date': start_date or '',
        'end_date': end_date or '',
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'performance_metrics.html', context)

def simulate_platform_metrics(request, campaign_id, platform):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    metrics, created = PlatformMetrics.objects.get_or_create(campaign=campaign, platform=platform)
    
    # Simulate metrics with platform-specific variations
    base_metrics = simulate_campaign_metrics(campaign)
    
    # Adjust metrics based on platform
    if platform == 'GOOGLE':
        base_metrics['ctr'] *= 1.2  # Google typically has higher CTR
        base_metrics['cpc'] *= 1.1  # Google typically has higher CPC
    elif platform == 'FACEBOOK':
        base_metrics['conversion_rate'] *= 1.15  # Facebook typically has better conversion rates
    elif platform == 'INSTAGRAM':
        base_metrics['impressions'] *= 1.3  # Instagram typically has higher reach
    
    # Update the metrics
    for key, value in base_metrics.items():
        setattr(metrics, key, value)
    metrics.save()
    
    messages.success(request, f'Metrics simulated successfully for {platform}!')
    return redirect('platforms_list')