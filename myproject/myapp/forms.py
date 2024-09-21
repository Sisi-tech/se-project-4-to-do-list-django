from django import forms 
from .models import ToDoItem

class ListForm(forms.ModelForm):
    class Meta:
        model = ToDoItem 
        fields = ["item"]
        