from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Note, NoteVersion
from .serializers import NoteSerializer, NoteVersionSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

class NoteVersionViewSet(viewsets.ModelViewSet):
    queryset = NoteVersion.objects.all()
    serializer_class = NoteVersionSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful'})
    else:
        return Response({'message': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'message': 'Username and password are required'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'message': 'User created successfully'})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_note(request):
    user = request.user
    request.data['owner'] = user.pk
    version = 1
    request.data['note_version'] = version
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        note = get_object_or_404(Note, id=serializer.data["id"])
        note_version = NoteVersion.objects.create(note=note, content=note.content, made_by=user, note_version=version)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note_by_id(request, id):
    note = get_object_or_404(Note, id=id)
    user = request.user
    if user != note.owner and user not in note.shared_with.all():
        return Response({'message': 'Access Forbidden'}, status=403)
    serializer = NoteSerializer(note)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def share_note(request):
    note_id = request.data.get('note_id')
    usernames = request.data.get('usernames')
    note = Note.objects.get(id=note_id)
    user = request.user
    if user != note.owner:
        return Response({'message': 'Access Forbidden'}, status=403)
    for username in usernames:
        user = User.objects.get(username=username)
        if not user:
            return Response({'message': 'User not found'}, status=404)
        note.shared_with.add(user)
    return Response({'message': 'Note shared successfully'})

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_note(request, id):
    note = get_object_or_404(Note, id=id)
    user = request.user
    if user != note.owner and user not in note.shared_with.all():
        return Response({'message': 'Access Forbidden'}, status=403)
    new_content = request.data.get('content')
    if new_content.startswith(note.content):
        note.content = new_content
        version = note.note_version + 1
        note.note_version = version
        note.save()
        note_version = NoteVersion.objects.create(note=note, content=new_content, made_by=user, note_version=version)
        return Response({'message': 'Note updated successfully', 'note_version_id': note_version.id})
    else:
        return Response({'message': 'Invalid update. Only new sentences can be added between existing lines.'}, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, id):
    note = get_object_or_404(Note, id=id)
    user = request.user
    if user != note.owner and user not in note.shared_with.all():
        return Response({'message': 'Access Forbidden'}, status=403)
    note_versions = NoteVersion.objects.filter(note=id)
    serializer = NoteVersionSerializer(note_versions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token = request.auth
    if token:
        token.delete()
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)
