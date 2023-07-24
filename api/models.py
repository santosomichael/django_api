from django.db import models
 
class Todo(models.Model):
    title = models.CharField(max_length=255)
    finished = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self) -> str:
        return self.title