from django.db import models

# Create your models here.
#Junesh is making some test model for migration purpose

class SomeModel(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)