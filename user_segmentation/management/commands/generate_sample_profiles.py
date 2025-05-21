from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_segmentation.models import UserProfile
import numpy as np
import random

NOMBRES = [
    'Sofía', 'Mateo', 'Valentina', 'Santiago', 'Isabella', 'Sebastián', 'Camila', 'Emiliano', 'Lucía', 'Martín',
    'Mariana', 'Gabriel', 'Sara', 'Samuel', 'Victoria', 'Daniel', 'Emma', 'David', 'Regina', 'Joaquín',
    'Antonella', 'Diego', 'Paula', 'Nicolás', 'Renata', 'Andrés', 'Mía', 'Felipe', 'Julieta', 'Juan',
    'Alejandra', 'Tomás', 'Carolina', 'Agustín', 'María', 'Pablo', 'Fernanda', 'Julián', 'Valeria', 'Manuel',
    'Daniela', 'Adrián', 'Gabriela', 'Javier', 'Ariana', 'Francisco', 'Elena', 'Miguel', 'Ana', 'Pedro'
]
APELLIDOS = [
    'García', 'Martínez', 'Rodríguez', 'López', 'Hernández', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Cruz',
    'Flores', 'Rivera', 'Gómez', 'Díaz', 'Torres', 'Vásquez', 'Castro', 'Morales', 'Romero', 'Jiménez',
    'Ruiz', 'Molina', 'Silva', 'Ortega', 'Rojas', 'Castillo', 'Ortiz', 'Suárez', 'Sosa', 'Delgado',
    'Ramos', 'Guerrero', 'Medina', 'Aguilar', 'Paredes', 'Cabrera', 'Vega', 'Campos', 'Reyes', 'Herrera',
    'Peña', 'Mendoza', 'Cortés', 'Luna', 'Ibarra', 'Navarro', 'Salazar', 'Miranda', 'Acosta', 'Fuentes'
]
DOMINIOS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com']

class Command(BaseCommand):
    help = 'Genera perfiles de usuario de muestra para pruebas con nombres realistas'

    def handle(self, *args, **kwargs):
        cantidad = 200
        usados = set()
        for i in range(cantidad):
            while True:
                nombre = random.choice(NOMBRES)
                apellido = random.choice(APELLIDOS)
                username = f"{nombre.lower()}.{apellido.lower()}"
                if username not in usados:
                    usados.add(username)
                    break
            dominio = random.choice(DOMINIOS)
            email = f"{username}@{dominio}"
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
                    'interes': random.choice(['tecnologia', 'deportes', 'moda', 'viajes', 'arte', 'cocina', 'música', 'lectura', 'cine', 'fotografía']),
                    'actividad': random.choice(['alta', 'media', 'baja']),
                    'dispositivo': random.choice(['movil', 'tablet', 'pc']),
                    'hora_activa': random.randint(0, 23),
                    'dias_activos': random.randint(1, 7),
                    'gasto_promedio': round(random.uniform(10, 2000), 2),
                    'frecuencia_compra': random.randint(1, 30),
                    'ultima_compra': random.randint(1, 365),
                    'clicks_previos': random.randint(0, 100),
                    'conversion_previo': random.choice([True, False])
                }
            )
            if created:
                self.stdout.write(f'Perfil creado para: {username}')
            else:
                self.stdout.write(f'Perfil ya existente para: {username}')
        self.stdout.write(self.style.SUCCESS('Perfiles de muestra realistas generados exitosamente')) 