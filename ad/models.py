from django.db import models

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

    def __str__(self):
        return self.name