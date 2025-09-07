"""
URL configuration for oatelier_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from oatelier_django.views import dashboard
=======
from oatelier_django.views import dashboard, inserir_lote_financeiro
>>>>>>> main
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('gerador/', TemplateView.as_view(template_name='gerador.html'), name='gerador'),
]
=======
    path('', dashboard, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('gerador/', admin.site.admin_view(lambda request: render(request, 'gerador.html')), name='gerador'),
    path('financeiro/inserir-lote/', inserir_lote_financeiro, name='inserir_lote_financeiro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

>>>>>>> main

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
