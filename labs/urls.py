from django.urls import path

from . import views

urlpatterns = [
    path("", views.LabsList.as_view()),
    path("<uuid:id>", views.LabDetail.as_view()),
]
