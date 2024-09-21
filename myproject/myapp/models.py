from django.db import models

# Create your models here.
class ToDoItem(models.Model):
    item = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.item 
