from django.contrib import admin
from .models import ToDoItem
from django.contrib.auth.admin import UserAdmin 

# Register your models here.
admin.site.register(ToDoItem)

class NewAdmin(UserAdmin):
    def get_form(self, request, obj=None, **Kwargs):
        form = super().get_form(request, obj, **Kwargs)
        is_superuser = request.user.is_superuser 

        if not is_superuser:
            form.base_fields['username'].disabled = True 
        return form 
    