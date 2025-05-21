from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import UserProfile, CampaignSegment, ModelMetrics, ModelFeature
from ad.models import Campaign
from .services import SegmentationService
import pandas as pd
import numpy as np

# Create your views here.

@login_required
def segment_campaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    
    if request.method == 'POST':
        service = SegmentationService(campaign)
        metrics = service.process_campaign()
        
        if metrics:
            messages.success(request, 'Segmentación completada exitosamente')
        else:
            messages.warning(request, 'Segmentación completada, pero no hay suficientes datos para calcular métricas')
        
        return redirect('user_segmentation:campaign_metrics', campaign_id=campaign_id)
    
    # Obtener segmentaciones existentes
    segments = CampaignSegment.objects.filter(campaign=campaign).order_by('-probability')
    
    return render(request, 'user_segmentation/segment.html', {
        'campaign': campaign,
        'segments': segments
    })

@login_required
def campaign_metrics(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    
    # Obtener métricas más recientes
    metrics = ModelMetrics.objects.filter(campaign=campaign).first()
    
    # Obtener importancia de características
    features = ModelFeature.objects.filter(campaign=campaign)
    
    # Obtener estadísticas de segmentación
    segments = CampaignSegment.objects.filter(campaign=campaign)
    total_users = segments.count()
    targeted_users = segments.filter(is_targeted=True).count()
    conversions = segments.filter(conversion_actual=True).count()
    
    # Obtener distribución de probabilidades
    probability_ranges = [
        ('0-20%', segments.filter(probability__lt=0.2).count()),
        ('20-40%', segments.filter(probability__gte=0.2, probability__lt=0.4).count()),
        ('40-60%', segments.filter(probability__gte=0.4, probability__lt=0.6).count()),
        ('60-80%', segments.filter(probability__gte=0.6, probability__lt=0.8).count()),
        ('80-100%', segments.filter(probability__gte=0.8).count()),
    ]
    probability_distribution = [
        {
            'range': r,
            'count': c,
            'percent': (c / total_users * 100) if total_users > 0 else 0
        } for r, c in probability_ranges
    ]

    return render(request, 'user_segmentation/metrics.html', {
        'campaign': campaign,
        'metrics': metrics,
        'features': features,
        'total_users': total_users,
        'targeted_users': targeted_users,
        'conversions': conversions,
        'probability_distribution': probability_distribution
    })

@login_required
def dashboard(request):
    # Obtener estadísticas generales
    total_campaigns = Campaign.objects.count()
    total_users = UserProfile.objects.count()
    total_segments = CampaignSegment.objects.count()
    
    # Obtener métricas promedio de todas las campañas
    avg_metrics = ModelMetrics.objects.aggregate(
        avg_accuracy=Avg('accuracy'),
        avg_precision=Avg('precision'),
        avg_recall=Avg('recall'),
        avg_f1_score=Avg('f1_score'),
        avg_auc_score=Avg('auc_score'),
        avg_conversion_rate=Avg('conversion_rate')
    )
    
    # Obtener campañas más recientes con sus métricas
    recent_campaigns = Campaign.objects.all().order_by('-id')[:5]
    campaign_metrics = []
    for campaign in recent_campaigns:
        metrics = ModelMetrics.objects.filter(campaign=campaign).first()
        if metrics:
            campaign_metrics.append({
                'campaign': campaign,
                'metrics': metrics
            })
    
    return render(request, 'user_segmentation/dashboard.html', {
        'total_campaigns': total_campaigns,
        'total_users': total_users,
        'total_segments': total_segments,
        'avg_metrics': avg_metrics,
        'campaign_metrics': campaign_metrics
    })
