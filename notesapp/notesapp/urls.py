"""
URL configuration for notesapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notes.views import (
    NoteViewSet, 
    NoteVersionViewSet,
    login_view,
    signup,
    create_note,
    get_note_by_id,
    share_note,
    update_note,
    get_note_version_history,
    logout_view
    )

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'note-versions', NoteVersionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', login_view),
    path('signup', signup),
    path('notes/create', create_note),
    path('notes/<int:id>', get_note_by_id),
    path('notes/share', share_note),
    path('notes/update/<int:id>', update_note),
    path('notes/version-history/<int:id>', get_note_version_history),
    path('logout', logout_view),
    path('admin', admin.site.urls),
]
