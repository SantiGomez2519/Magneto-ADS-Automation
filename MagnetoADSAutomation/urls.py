"""
URL configuration for MagnetoADSAutomation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from home.views import home
from user.views import login_page
from ad.views import add
from ad import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    path("", include("user.urls")),
    path("home/", home, name="home"),
    path("login/", login_page, name="login"),
    path("add/", add, name="add"),
    path('campaign/edit/<int:id>/', views.edit_campaign, name='edit_campaign'),
    path('campaign/delete/<int:campaign_id>/', views.delete_campaign, name='delete_campaign'),
    path("ad/", include("ad.urls")),
    path("segmentation/", include("user_segmentation.urls")),

    path("__reload__/", include("django_browser_reload.urls")),
]

# Agregar rutas estáticas después de definir urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)