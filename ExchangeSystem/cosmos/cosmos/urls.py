"""cosmos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from transfer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sender-wallets/', views.SenderWalletList.as_view()),
    path('api/sender-wallet/<int:pk>/', views.SenderWalletObject.as_view()),
    path('api/receiver-wallets/', views.ReceiverWalletList.as_view()),
    path('api/receiver-wallet/<int:pk>/', views.ReceiverWalletObject.as_view()),
    path('api-auth/', include('rest_framework.urls'))
]
