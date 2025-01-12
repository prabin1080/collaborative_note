from django.urls import path
from .views import (
    note_view, NoteListCreateView, NoteDetailView,
)

urlpatterns = [
    path('', NoteListCreateView.as_view(), name='note-list-create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path("ui/<int:note_id>/", note_view, name="note-ui"),
]
