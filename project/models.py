from django.db import models

# Create your models here.


class Project(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False)
    last_update = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.created_at} {self.name}"
