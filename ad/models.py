from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('IT', 'Technology'),
        ('MK', 'Marketing'),
        ('AD', 'Administration'),
        ('SL', 'Sales'),
        ('HR', 'Human Resources'),
        ('FI', 'Finance'),
        ('ED', 'Education'),
        ('HL', 'Healthcare'),
        ('OT', 'Other'),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('NONE', 'None'),
        ('HS', 'High School'),
        ('TEC', 'Technical'),
        ('TCH', 'Technologist'),
        ('UNI', 'University'),
        ('POS', 'Postgraduate'),
        ('PHD', 'Doctorate'),
    ]

    MODALITY_CHOICES = [
        ('ONSITE', 'On-site'),
        ('REMOTE', 'Remote'),
        ('HYBRID', 'Hybrid'),
        ('FLEX', 'Flexible'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('NONE', 'No experience'),
        ('1-3', '1 to 3 years'),
        ('4-7', '4 to 7 years'),
        ('8+', '8 or more years'),
    ]
    
    LOCATION_CHOICES = [
    ('AR', 'Argentina'),
    ('BR', 'Brazil'),
    ('CA', 'Canada'),
    ('CL', 'Chile'),
    ('CO', 'Colombia'),
    ('MX', 'Mexico'),
    ('US', 'United States'),
    ('VE', 'Venezuela'),

    ('DE', 'Germany'),
    ('ES', 'Spain'),
    ('FR', 'France'),
    ('GB', 'United Kingdom'),
    ('IT', 'Italy'),
    ('NL', 'Netherlands'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),

    ('CN', 'China'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('JP', 'Japan'),
    ('KR', 'South Korea'),
    ('PH', 'Philippines'),
    ('SG', 'Singapore'),
    ('TH', 'Thailand'),
    ]

    PLATFORM_CHOICES = [
        ('GOOGLE', 'Google'),
        ('FACEBOOK', 'Facebook'),
        ('INSTAGRAM', 'Instagram'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='campaign_images/')
    schedule = models.DateField()
    end_schedule = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    education_level = models.CharField(max_length=10, choices=EDUCATION_LEVEL_CHOICES)
    modality = models.CharField(max_length=10, choices=MODALITY_CHOICES)
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES, default= 'Colmbia')
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    
    # Nuevos campos para plataformas
    platform1 = models.CharField(max_length=10, choices=PLATFORM_CHOICES, null=True, blank=True)
    platform2 = models.CharField(max_length=10, choices=PLATFORM_CHOICES, null=True, blank=True)
    platform3 = models.CharField(max_length=10, choices=PLATFORM_CHOICES, null=True, blank=True)

    def clean(self):
        # Validar que al menos una plataforma esté seleccionada
        if not self.platform1 and not self.platform2 and not self.platform3:
            raise ValidationError('At least one platform must be selected.')
        
        # Validar que no haya plataformas duplicadas
        platforms = [p for p in [self.platform1, self.platform2, self.platform3] if p]
        if len(platforms) != len(set(platforms)):
            raise ValidationError('Each platform can only be selected once.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AdMetrics(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, related_name='metrics')
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    ctr = models.FloatField()
    conversions = models.IntegerField()
    conversion_rate = models.FloatField()
    cpc = models.FloatField()
    cpa = models.FloatField()
    spend = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metrics for {self.campaign.name}"

class PlatformMetrics(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='platform_metrics')
    platform = models.CharField(max_length=10, choices=Campaign.PLATFORM_CHOICES)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    ctr = models.FloatField()
    conversions = models.IntegerField()
    conversion_rate = models.FloatField()
    cpc = models.FloatField()
    cpa = models.FloatField()
    spend = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'platform')

    def __str__(self):
        return f"Metrics for {self.campaign.name} on {self.platform}"