from django.shortcuts import render, get_object_or_404, redirect 
from .models import ToDoItem
from .serializers import ItemSerializer
from django.contrib import messages 
from .forms import ListForm 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.views import APIView 
from django.core.paginator import Paginator, EmptyPage

def display_to_do_list(request):
    if request.method == 'POST':
        item_name = request.POST.get("item")
        if item_name:
            if ToDoItem.objects.filter(item=item_name).exists():
                messages.error(request, "This item already exists in the list")
            else:
                ToDoItem.objects.create(item=item_name)
                return redirect('display_to_do_list')
        
    todo_items = ToDoItem.objects.all()
    context = {"todo_items": todo_items}
    return render(request, "home.html", context)


class DisplayList(APIView):
    def get(self, request):
        todo_items = ToDoItem.objects.all()
        search = request.query_params.get('search')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        
        if search:
            todo_items = todo_items.filter(title__icontains=search)
        
        paginator = Paginator(todo_items, per_page=perpage)
        try:
            todo_items = paginator.page(number=page)
        except EmptyPage:
            todo_items = []

        serializer = ItemSerializer(todo_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Item(APIView):
    def get(self, request, pk):
        item = get_object_or_404(ToDoItem, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk):
        item = get_object_or_404(ToDoItem, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        item = get_object_or_404(ToDoItem, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)