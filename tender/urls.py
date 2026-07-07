from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_order, name="create"),
    path("result/<int:order_id>/", views.result, name="result"),
    path("download/<int:order_id>/", views.download_pdf, name="download"),
]
