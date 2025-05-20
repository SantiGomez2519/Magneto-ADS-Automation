from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.IntegerField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    interes = models.CharField(max_length=50)
    actividad = models.CharField(max_length=10, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')])
    dispositivo = models.CharField(max_length=10, choices=[('movil', 'Móvil'), ('tablet', 'Tablet'), ('pc', 'PC')])
    hora_activa = models.IntegerField()
    dias_activos = models.IntegerField()
    gasto_promedio = models.DecimalField(max_digits=10, decimal_places=2)
    frecuencia_compra = models.IntegerField()
    ultima_compra = models.IntegerField()
    clicks_previos = models.IntegerField()
    conversion_previo = models.BooleanField()

    def __str__(self):
        return f"Perfil de {self.user.username}"

class CampaignSegment(models.Model):
    campaign = models.ForeignKey('ad.Campaign', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_targeted = models.BooleanField(default=False)
    conversion_actual = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together = ('campaign', 'user_profile')

    def __str__(self):
        return f"Segmento para {self.campaign.name} - {self.user_profile.user.username}"

class ModelMetrics(models.Model):
    campaign = models.ForeignKey('ad.Campaign', on_delete=models.CASCADE)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    auc_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_users = models.IntegerField()
    targeted_users = models.IntegerField()
    conversions = models.IntegerField()
    conversion_rate = models.FloatField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Métricas para {self.campaign.name} - {self.created_at}"

class ModelFeature(models.Model):
    name = models.CharField(max_length=100)
    importance = models.FloatField()
    campaign = models.ForeignKey('ad.Campaign', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-importance']

    def __str__(self):
        return f"{self.name} - {self.importance:.2f}"
