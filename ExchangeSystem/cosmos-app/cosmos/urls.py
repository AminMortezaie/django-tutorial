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
from cardano import views as cardano_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Transfer API List",
        default_version='v1',
        description="Transfer API List",
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
)


urlpatterns = [
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # <-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/cosmos-sender-wallets/', views.SenderWalletList.as_view()),
    path('api/cosmos-sender-wallets/<int:pk>/', views.SenderWalletObject.as_view()),
    path('api/cosmos-receiver-wallets/', views.ReceiverWalletList.as_view()),
    path('api/cosmos-receiver-wallets/<int:pk>/', views.ReceiverWalletObject.as_view()),
    path('api/cosmos-transactions/', views.CreateTransactionsList.as_view()),
    path('api/cosmos-transactions/<int:pk>/', views.CreateTransactionObject.as_view()),

    path('api/cardano-sender-wallets/', cardano_views.CardanoSenderWalletList.as_view()),
    path('api/cardano-sender-wallets/<int:pk>/', cardano_views.CardanoSenderWalletObject.as_view()),
    path('api/cardano-receiver-wallets/', cardano_views.CardanoReceiverWalletList.as_view()),
    path('api/cardano-receiver-wallets/<int:pk>/', cardano_views.CardanoReceiverWalletObject.as_view()),
    path('api/cardano-transactions/', cardano_views.CardanoCreateTransactionsList.as_view()),
    path('api/cardano-transactions/<int:pk>/', cardano_views.CardanoCreateTransactionObject.as_view()),

    path('api-auth/', include('rest_framework.urls')),
]
