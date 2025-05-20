from django.core.management.base import BaseCommand
from ad.models import Campaign
from user_segmentation.services import SegmentationService
from django.db import transaction

class Command(BaseCommand):
    help = 'Actualiza todas las campañas existentes con el modelo mejorado'

    def handle(self, *args, **kwargs):
        campaigns = Campaign.objects.all()
        total_campaigns = campaigns.count()
        
        self.stdout.write(f'Iniciando actualización de {total_campaigns} campañas...')
        
        for i, campaign in enumerate(campaigns, 1):
            try:
                with transaction.atomic():
                    # Crear instancia del servicio de segmentación
                    service = SegmentationService(campaign)
                    
                    # Procesar la campaña
                    metrics = service.process_campaign()
                    
                    if metrics:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Campaña {i}/{total_campaigns}: {campaign.name} actualizada exitosamente. '
                                f'Precisión: {metrics.accuracy:.2f}, Recall: {metrics.recall:.2f}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Campaña {i}/{total_campaigns}: {campaign.name} actualizada, '
                                'pero no hay suficientes datos para métricas'
                            )
                        )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error al procesar la campaña {campaign.name}: {str(e)}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('Proceso de actualización completado')) 