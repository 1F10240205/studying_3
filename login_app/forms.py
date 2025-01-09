from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class ArticleContents(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    posted_at  = models.DateTimeField(default=timezone.now)
    published_at  = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class ArticleComment(models.Model):
    text = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(ArticleContents, related_name='comments', on_delete=models.CASCADE)