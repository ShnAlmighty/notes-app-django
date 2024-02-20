from django.test import TestCase
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Note, NoteVersion

class NoteAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
            owner=self.user,
            note_version=1
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
    
    def test_get_note_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(f'/notes/{self.note.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Note')

    def test_get_note_by_id_failure_no_auth_token(self):
        response = self.client.get(f'/notes/{self.note.id}')
        self.assertEqual(response.status_code, 401)
    
    def test_create_note(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.client.force_authenticate(user=self.user)
        data = {'title': 'New Note', 'content': 'This is a new note.'}
        response = self.client.post('/notes/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)

    def test_create_note_failure_content_not_provided(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.client.force_authenticate(user=self.user)
        data = {'title': 'New Note'}
        response = self.client.post('/notes/create', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_update_note(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.client.force_authenticate(user=self.user)
        data = {'content': 'This is a test note. This is an updated note.'}
        response = self.client.put(f'/notes/update/{self.note.id}', data, format='json')
        self.note = get_object_or_404(Note, id=self.note.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.note.note_version, 2)
        self.note_version = get_object_or_404(NoteVersion, note=self.note.id)
        print("NOTE_VERSION=", self.note_version)

    def test_update_note_failure_for_new_content(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.client.force_authenticate(user=self.user)
        data = {'content': 'This is an updated note without failure content'}
        response = self.client.put(f'/notes/update/{self.note.id}', data, format='json')
        self.note = get_object_or_404(Note, id=self.note.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.note.note_version, 1)

    def test_logout_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(f'/logout')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
