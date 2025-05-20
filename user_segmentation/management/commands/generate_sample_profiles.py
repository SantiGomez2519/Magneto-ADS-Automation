from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_segmentation.models import UserProfile
import numpy as np
import random

class Command(BaseCommand):
    help = 'Genera perfiles de usuario de muestra para pruebas'

    def handle(self, *args, **kwargs):
        # Crear usuarios de muestra si no existen
        for i in range(1, 11):  # Crear 10 usuarios de muestra
            username = f'usuario{i}'
            email = f'usuario{i}@ejemplo.com'
            
            # Crear usuario si no existe
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
                defaults={
                    'password': 'pbkdf2_sha256$600000$defaultpassword',
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Usuario creado: {username}')
            
            # Crear perfil de usuario si no existe
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'edad': random.randint(18, 65),
                    'genero': random.choice(['M', 'F']),
                    'interes': random.choice(['tecnologia', 'deportes', 'moda', 'viajes']),
                    'actividad': random.choice(['alta', 'media', 'baja']),
                    'dispositivo': random.choice(['movil', 'tablet', 'pc']),
                    'hora_activa': random.randint(0, 23),
                    'dias_activos': random.randint(1, 7),
                    'gasto_promedio': round(random.uniform(10, 1000), 2),
                    'frecuencia_compra': random.randint(1, 30),
                    'ultima_compra': random.randint(1, 365),
                    'clicks_previos': random.randint(0, 50),
                    'conversion_previo': random.choice([True, False])
                }
            )
            
            if created:
                self.stdout.write(f'Perfil creado para: {username}')
            else:
                self.stdout.write(f'Perfil ya existente para: {username}')
        
        self.stdout.write(self.style.SUCCESS('Perfiles de muestra generados exitosamente')) 