# Generated by Django 5.1.6 on 2025-05-21 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0010_admetrics'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('GOOGLE', 'Google'), ('FACEBOOK', 'Facebook'), ('INSTAGRAM', 'Instagram')], max_length=10)),
                ('impressions', models.IntegerField()),
                ('clicks', models.IntegerField()),
                ('ctr', models.FloatField()),
                ('conversions', models.IntegerField()),
                ('conversion_rate', models.FloatField()),
                ('cpc', models.FloatField()),
                ('cpa', models.FloatField()),
                ('spend', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='platform_metrics', to='ad.campaign')),
            ],
            options={
                'unique_together': {('campaign', 'platform')},
            },
        ),
    ]
