from crypto import views
from django.urls import path

app_name = "crypto"
urlpatterns = [
    path("", views.index, name="index"),
    path('process_token/', views.process_token, name='process_token'),
    path('transaction/', views.transaction_view, name='transaction'),
    path('wallet/', views.wallet_view, name='wallet'),
    path("reset_session/", views.reset_session, name="reset_session"),
    
]