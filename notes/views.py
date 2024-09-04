from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Note
from .serializers import NoteSerializer
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
def notes_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    elif request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def list_notes(request):
    if request.method == 'GET':
        notes = Note.objects.all()  # Fetch all notes from the database
        notes_list = []
        for note in notes:
            notes_list.append({
                'id': note.id,
                'title': note.title,
                'body': note.body,
                'created_at': note.created_at,
                'updated_at': note.updated_at,
            })
        return JsonResponse(notes_list, safe=False)  # Return the list as JSON
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_note_by_id(request, id):
    try:
        note = Note.objects.get(pk=id)
        serializer = NoteSerializer(note)
        return JsonResponse(serializer.data, safe=False)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

def query_notes_by_title(request,title):
    print(request)
    #title_substring = request.GET.get('title', None)
    if title:
        notes = Note.objects.filter(title__icontains=title)
        serializer = NoteSerializer(notes, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'error': 'No title provided'}, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
def update_note(request, id):
    if request.method == 'PUT':
        try:
            note = Note.objects.get(pk=id)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

        data = json.loads(request.body)
        serializer = NoteSerializer(note, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
