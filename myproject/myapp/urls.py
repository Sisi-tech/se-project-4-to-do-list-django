from django.urls import path
from . import views 
from django.conf.urls.static import static

urlpatterns = [
    path('', views.display_to_do_list, name='display_to_do_list'),
    path('api/todos/', views.DisplayList.as_view(), name='display_list'),
    path('api/todos/<int:pk>/', views.Item.as_view(), name='item'),
]