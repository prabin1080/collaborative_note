from django.urls import path
from .views import note_view

urlpatterns = [
    path("<int:note_id>/", note_view, name="note"),
]
