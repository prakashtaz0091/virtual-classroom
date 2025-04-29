from django.urls import path
from . import views

urlpatterns = [
    path("pay/<int:note_id>/", views.initiate_payment, name="esewa-pay"),
    path("success/<str:transaction_uuid>/", views.payment_success, name="esewa-success"),
    path("failure/<str:transaction_uuid>/", views.payment_failure, name="esewa-failure"),
]
