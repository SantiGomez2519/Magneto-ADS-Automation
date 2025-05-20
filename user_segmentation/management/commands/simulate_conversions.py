from django.core.management.base import BaseCommand
from user_segmentation.models import CampaignSegment
import random

class Command(BaseCommand):
    help = 'Simula conversiones reales en los segmentos de campaña para pruebas de métricas.'

    def handle(self, *args, **kwargs):
        segmentos = CampaignSegment.objects.all()
        total = segmentos.count()
        actualizados = 0
        for segmento in segmentos:
            # Simular conversión con probabilidad 30%
            conversion = random.choices([True, False], weights=[0.3, 0.7])[0]
            segmento.conversion_actual = conversion
            segmento.save()
            actualizados += 1
        self.stdout.write(self.style.SUCCESS(f'Se actualizaron {actualizados} segmentos de campaña con conversiones simuladas.')) 