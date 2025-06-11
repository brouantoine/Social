from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('STUDENT', 'Élève'),
        ('TEACHER', 'Enseignant'),
        ('TUTOR', 'Tuteur'),
        ('ADMIN', 'Administrateur'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    school = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=50, blank=True)  
    verified = models.BooleanField(default=False)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class EducationalPost(models.Model):
    POST_TYPES = (
        ('LESSON', 'Leçon'),
        ('QUIZ', 'Quiz'),
        ('RESOURCE', 'Ressource'),
        ('DISCUSSION', 'Discussion'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    attachment = models.FileField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(EducationalPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class VirtualClass(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_classes')
    students = models.ManyToManyField(User, related_name='joined_classes')
    schedule = models.JSONField()  # Ex: {"days": ["Mon", "Wed"], "time": "15:00"}
    created_at = models.DateTimeField(auto_now_add=True)

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='GroupMembership')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('NEW_POST', 'Nouveau post'),
        ('CLASS_UPDATE', 'Mise à jour de classe'),
        ('MESSAGE', 'Message privé'),
        ('GROUP_INVITE', 'Invitation à un groupe'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
    content = models.JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)