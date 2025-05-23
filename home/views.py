from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import csv
from django.http import JsonResponse, HttpResponse
from ad.models import Campaign, AdInteraction
from django.db.models import Sum
from django.utils.dateparse import parse_date
from datetime import datetime
from django.utils import timezone


def interaction_dashboard(request):
    data = (
        AdInteraction.objects
        .values('ad__name')  # ✅ CAMBIADO
        .annotate(
            total_impressions=Sum('impressions'),
            total_clicks=Sum('clicks'),
            total_conversions=Sum('conversions'),
        )
    )
    return render(request, 'home/home.html', {'ad_data': data})


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ad_interactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ad Name', 'Impressions', 'Clicks', 'Conversions'])

    interactions = (
        AdInteraction.objects
        .values('ad__name')  # ✅ CAMBIADO
        .annotate(
            total_impressions=Sum('impressions'),
            total_clicks=Sum('clicks'),
            total_conversions=Sum('conversions'),
        )
    )

    for row in interactions:
        writer.writerow([
            row['ad__name'],  # ✅ CAMBIADO
            row['total_impressions'],
            row['total_clicks'],
            row['total_conversions']
        ])

    return response


@login_required(login_url='login')
def home(request):
    interactions = AdInteraction.objects.select_related('ad').all()

    platform_data = {}

    for interaction in interactions:
        ad = interaction.ad
        platforms = [ad.platform1, ad.platform2, ad.platform3]

        platform = interaction.platform
        if platform:
            if platform not in platform_data:
                platform_data[platform] = {
                    'impressions': 0,
                    'clicks': 0,
                    'conversions': 0
                }
            platform_data[platform]['impressions'] += interaction.impressions
            platform_data[platform]['clicks'] += interaction.clicks
            platform_data[platform]['conversions'] += interaction.conversions



    # Preparar datos para gráficos
    platforms = list(platform_data.keys())
    impressions = [platform_data[p]['impressions'] for p in platforms]
    clicks = [platform_data[p]['clicks'] for p in platforms]
    conversions = [platform_data[p]['conversions'] for p in platforms]

    context = {
        'platform_data': platform_data,
        'platforms': platforms,
        'impressions': impressions,
        'clicks': clicks,
        'conversions': conversions,
    }

    return render(request, "home.html", context)



@login_required(login_url='login')
def report_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    export = request.GET.get('export')

    interactions = AdInteraction.objects.select_related('ad')

    if start_date:
        interactions = interactions.filter(date__gte=parse_date(start_date))
    if end_date:
        interactions = interactions.filter(date__lte=parse_date(end_date))
    if category:
        interactions = interactions.filter(ad__category=category)

    summary = interactions.aggregate(
        total_impressions=Sum('impressions') or 0,
        total_clicks=Sum('clicks') or 0,
        total_conversions=Sum('conversions') or 0
    )

    if export == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="detailed_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Ad Name', 'Impressions', 'Clicks', 'Conversions'])

        for i in interactions.values('ad__name').annotate(
            impressions=Sum('impressions'),
            clicks=Sum('clicks'),
            conversions=Sum('conversions')
        ):
            writer.writerow([i['ad__name'], i['impressions'], i['clicks'], i['conversions']])
        return response

    categories = Campaign.objects.values_list('category', flat=True).distinct()

    context = {
        'summary': summary,
        'interactions': interactions,
        'categories': categories,
        'start_date': start_date,
        'end_date': end_date,
        'selected_category': category,
    }

    return render(request, 'report.html', context)
