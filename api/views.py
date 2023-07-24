from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import serializers
from rest_framework import status
 
@api_view(['POST'])
def create(request):
    todo = TodoSerializer(data=request.data)
 
    if todo.is_valid():
        todo.save()
        return Response(todo.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def read_all(request):
    # checking for the parameters from the URL
    if request.query_params:
        todoList = Todo.objects.filter(**request.query_params.dict())
    else:
        todoList = Todo.objects.all()
 
    # if there is something in items else raise error
    if todoList:
        serializer = TodoSerializer(todoList, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
def update(request, pk):
    todo = Todo.objects.get(pk=pk)
    data = TodoSerializer(instance=todo, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete(request, pk):
    item = get_object_or_404(Todo, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)