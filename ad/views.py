from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Campaign
from django.db.models import Q
from django.core.exceptions import ValidationError


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