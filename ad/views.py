from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Campaign


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

        print("Data received:", name, description, image, schedule)  

        # Validar que los campos no estén vacíos
        if not name or not description or not image or not schedule:
            messages.error(request, "All fields are required.")
            return render(request, "ad/add.html")

        # Guardar la campaña
        campaign = Campaign.objects.create(
            name=name,
            description=description,
            image=image,
            schedule=schedule
        )

        return render(request, "campaign_success.html")

    return render(request, "ad/add.html")

def edit_campaign(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    if request.method == 'POST':
        # Actualizamos los datos de la campaña con lo recibido del formulario
        campaign.name = request.POST.get('name')
        campaign.description = request.POST.get('description')
        campaign.schedule = request.POST.get('schedule')
        if request.FILES.get('image'):
            campaign.image = request.FILES.get('image')
        campaign.save()
        messages.success(request, "Campaña actualizada correctamente.")
        return redirect('campaign_list')
    return render(request, 'edit_campaign.html', {'campaign': campaign})

def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, "campaign_list.html", {"campaigns": campaigns})

def delete_campaign(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, id=campaign_id)
        campaign.delete()
    return redirect('campaign_list')