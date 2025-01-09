from django.shortcuts import render, get_object_or_404
from .models import Note

def note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, "notes/note.html", {"note": note})
