from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
from .models import UserProfile, CampaignSegment, ModelMetrics, ModelFeature

class SegmentationService:
    def __init__(self, campaign):
        self.campaign = campaign
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_names = [
            'edad', 'genero', 'hora_activa', 'dias_activos',
            'gasto_promedio', 'frecuencia_compra', 'ultima_compra',
            'clicks_previos', 'conversion_previo'
        ]

    def prepare_data(self):
        user_profiles = UserProfile.objects.all()
        X = []
        y = []
        
        for profile in user_profiles:
            # Obtener conversiones históricas para este usuario
            historical_conversions = CampaignSegment.objects.filter(
                user_profile=profile,
                conversion_actual__isnull=False
            ).values_list('conversion_actual', flat=True)
            
            # Si no hay datos históricos, usar una conversión aleatoria
            if not historical_conversions:
                conversion = np.random.choice([True, False], p=[0.3, 0.7])
            else:
                conversion = np.random.choice(historical_conversions)
            
            features = [
                profile.edad,
                1 if profile.genero == 'M' else 0,
                profile.hora_activa,
                profile.dias_activos,
                float(profile.gasto_promedio),
                profile.frecuencia_compra,
                profile.ultima_compra,
                profile.clicks_previos,
                1 if profile.conversion_previo else 0
            ]
            
            X.append(features)
            y.append(1 if conversion else 0)
        
        return np.array(X), np.array(y)

    def train_model(self):
        X, y = self.prepare_data()
        self.model.fit(X, y)
        
        # Guardar importancia de características
        feature_importances = self.model.feature_importances_
        for name, importance in zip(self.feature_names, feature_importances):
            ModelFeature.objects.create(
                name=name,
                importance=importance,
                campaign=self.campaign
            )

    def predict(self):
        user_profiles = UserProfile.objects.all()
        X = []
        profiles = []
        
        for profile in user_profiles:
            features = [
                profile.edad,
                1 if profile.genero == 'M' else 0,
                profile.hora_activa,
                profile.dias_activos,
                float(profile.gasto_promedio),
                profile.frecuencia_compra,
                profile.ultima_compra,
                profile.clicks_previos,
                1 if profile.conversion_previo else 0
            ]
            X.append(features)
            profiles.append(profile)
        
        X = np.array(X)
        probabilities = self.model.predict_proba(X)[:, 1]
        
        # Guardar predicciones
        for profile, prob in zip(profiles, probabilities):
            CampaignSegment.objects.update_or_create(
                campaign=self.campaign,
                user_profile=profile,
                defaults={
                    'probability': prob,
                    'is_targeted': prob > 0.5  # Considerar como objetivo si la probabilidad > 0.5
                }
            )

    def calculate_metrics(self):
        segments = CampaignSegment.objects.filter(campaign=self.campaign)
        if not segments.exists():
            return None
        
        # Calcular métricas básicas
        total_users = segments.count()
        targeted_users = segments.filter(is_targeted=True).count()
        conversions = segments.filter(conversion_actual=True).count()
        conversion_rate = conversions / targeted_users if targeted_users > 0 else 0
        
        # Calcular métricas del modelo si hay conversiones registradas
        if segments.filter(conversion_actual__isnull=False).exists():
            y_true = list(segments.filter(conversion_actual__isnull=False).values_list('conversion_actual', flat=True))
            y_pred = list(segments.filter(conversion_actual__isnull=False).values_list('is_targeted', flat=True))
            
            metrics = ModelMetrics.objects.create(
                campaign=self.campaign,
                accuracy=accuracy_score(y_true, y_pred),
                precision=precision_score(y_true, y_pred, zero_division=0),
                recall=recall_score(y_true, y_pred, zero_division=0),
                f1_score=f1_score(y_true, y_pred, zero_division=0),
                auc_score=roc_auc_score(y_true, y_pred),
                total_users=total_users,
                targeted_users=targeted_users,
                conversions=conversions,
                conversion_rate=conversion_rate
            )
            return metrics
        
        return None

    def process_campaign(self):
        self.train_model()
        self.predict()
        return self.calculate_metrics() 