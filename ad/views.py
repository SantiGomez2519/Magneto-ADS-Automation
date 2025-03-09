from django.shortcuts import render, redirect
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
def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, "campaign_list.html", {"campaigns": campaigns})