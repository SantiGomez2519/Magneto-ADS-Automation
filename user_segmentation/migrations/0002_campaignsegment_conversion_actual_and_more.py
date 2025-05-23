# Generated by Django 5.1.6 on 2025-05-20 04:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0009_delete_campaigntarget_delete_targetuser'),
        ('user_segmentation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignsegment',
            name='conversion_actual',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='campaignsegment',
            name='is_targeted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ModelFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('importance', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.campaign')),
            ],
            options={
                'ordering': ['-importance'],
            },
        ),
        migrations.CreateModel(
            name='ModelMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accuracy', models.FloatField()),
                ('precision', models.FloatField()),
                ('recall', models.FloatField()),
                ('f1_score', models.FloatField()),
                ('auc_score', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_users', models.IntegerField()),
                ('targeted_users', models.IntegerField()),
                ('conversions', models.IntegerField()),
                ('conversion_rate', models.FloatField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.campaign')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
