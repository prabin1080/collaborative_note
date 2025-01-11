from django.shortcuts import render, get_object_or_404
from .models import Note
from rest_framework import generics, permissions
from .serializers import NoteSerializer


def note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, "notes/note.html", {"note": note})



class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
