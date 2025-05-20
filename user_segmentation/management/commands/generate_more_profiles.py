from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_segmentation.models import UserProfile
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Genera perfiles de usuario adicionales con datos variados'

    def handle(self, *args, **kwargs):
        # Lista de intereses comunes
        intereses = [
            'Tecnología', 'Moda', 'Deportes', 'Música', 'Cine', 'Libros',
            'Gastronomía', 'Viajes', 'Fitness', 'Arte', 'Fotografía',
            'Videojuegos', 'Cocina', 'Mascotas', 'Jardinería'
        ]

        # Generar 50 usuarios adicionales
        for i in range(50):
            username = f'usuario_extra_{i+1}'
            email = f'{username}@example.com'
            
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123'
            )
            
            # Crear perfil con datos aleatorios
            UserProfile.objects.create(
                user=user,
                edad=random.randint(18, 65),
                genero=random.choice(['M', 'F']),
                interes=random.choice(intereses),
                actividad=random.choice(['alta', 'media', 'baja']),
                dispositivo=random.choice(['movil', 'tablet', 'pc']),
                hora_activa=random.randint(0, 23),
                dias_activos=random.randint(1, 7),
                gasto_promedio=round(random.uniform(10.0, 1000.0), 2),
                frecuencia_compra=random.randint(1, 30),
                ultima_compra=random.randint(1, 90),
                clicks_previos=random.randint(0, 100),
                conversion_previo=random.choice([True, False])
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Perfil creado exitosamente para {username}')
            ) 