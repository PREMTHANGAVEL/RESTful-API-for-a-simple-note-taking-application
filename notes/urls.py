# app/urls.py
from django.urls import path
from .views import get_note_by_id, query_notes_by_title, update_note, notes_view, list_notes

urlpatterns = [
    path('POST/notes/', notes_view, name='create_note'),
    path('GET/notes/<int:id>/', get_note_by_id, name='get_note_by_id'),
    path('GET/notes/title/<str:title>/', query_notes_by_title, name='query_notes_by_title'),  # Ensure this is correct
    path('PUT/update/<int:id>/', update_note, name='update_note'),
    path('GET/noteslist/', list_notes, name='list_notes'),
]
