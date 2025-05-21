from user_segmentation.models import ModelFeature
from django.db.models import Max

# Encuentra el id más reciente para cada (campaign, name)
latest_ids = ModelFeature.objects.values('campaign', 'name').annotate(latest_id=Max('id')).values_list('latest_id', flat=True)

# Elimina todos los ModelFeature que no sean el más reciente para ese (campaign, name)
qs = ModelFeature.objects.exclude(id__in=list(latest_ids))
deleted_count, _ = qs.delete()
print(f"Deleted {deleted_count} duplicate ModelFeature entries.") 