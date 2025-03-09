from django.db import models

# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='campaign_images/')
    schedule = models.DateField()

    def __str__(self):
        return self.name