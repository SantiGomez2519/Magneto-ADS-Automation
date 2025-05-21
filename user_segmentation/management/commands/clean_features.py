from django.core.management.base import BaseCommand
from user_segmentation.models import ModelFeature
from django.db.models import Max

class Command(BaseCommand):
    help = 'Elimina duplicados de ModelFeature, dejando solo el más reciente por campaña y nombre de feature.'

    def handle(self, *args, **options):
        latest_ids = ModelFeature.objects.values('campaign', 'name').annotate(latest_id=Max('id')).values_list('latest_id', flat=True)
        qs = ModelFeature.objects.exclude(id__in=list(latest_ids))
        deleted_count, _ = qs.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} duplicate ModelFeature entries.')) 