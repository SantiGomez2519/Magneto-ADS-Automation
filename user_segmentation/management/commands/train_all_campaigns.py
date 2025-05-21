from django.core.management.base import BaseCommand
from ad.models import Campaign
from user_segmentation.services import SegmentationService

class Command(BaseCommand):
    help = 'Entrena (segmenta) todas las campañas existentes con los usuarios actuales.'

    def handle(self, *args, **kwargs):
        campaigns = Campaign.objects.all()
        total = campaigns.count()
        entrenadas = 0
        for campaign in campaigns:
            service = SegmentationService(campaign)
            metrics = service.process_campaign()
            if metrics:
                entrenadas += 1
                self.stdout.write(self.style.SUCCESS(f'Segmentación/entrenamiento completado para: {campaign.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Sin datos suficientes para: {campaign.name}'))
        self.stdout.write(self.style.SUCCESS(f'Entrenamiento masivo completado. Campañas entrenadas: {entrenadas}/{total}')) 