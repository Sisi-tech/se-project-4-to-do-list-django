from django.shortcuts import render, get_object_or_404
from .models import List 
from .serializers import ItemSerializer
from .forms import ListForm 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from django.core.paginator import Paginator, EmptyPage

def display_to_do_list(request):
    list = List.objects.all()
    context = {"list": list}
    return render(request, "home.html", context)

class DisplayList(APIView):
    def get(self, request):
        list = List.objects.all()
        search = request.query_params.get('search')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        
        if search:
            list = list.filter(title__icontains=search)
        
        paginator = Paginator(list, per_page=perpage)
        try:
            list = paginator.page(number=page)
        except EmptyPage:
            list = []

        serializer = ItemSerializer(list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Item(APIView):
    def get(self, request, pk):
        item = List.objects.get(pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk):
        item = List.objects.get(pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        item = List.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)