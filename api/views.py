from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import  status, generics
from datetime import datetime

class TodoList(generics.GenericAPIView):
   serializer_class = TodoSerializer
   queryset = Todo.objects.all()
    
   def get(self, request):
      todoList = Todo.objects.all()
      serializer = self.serializer_class(todoList, many=True)
      return Response({
         "status": "success",
         "total": todoList.count(),
         "data": serializer.data
      })
      
   def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
      else:
         return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      
class TodoDetail(generics.GenericAPIView):
   queryset = Todo.objects.all()
   serializer_class = TodoSerializer
   
   def get_todo(self, pk):
      try:
         return Todo.objects.get(pk=pk)
      except:
         return None
      
   def get(self, request, pk):
      todo = self.get_todo(pk=pk)
      if todo == None:
         return Response({"status": "fail", "message": f"Todo with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

      serializer = self.serializer_class(todo)
      return Response({"status": "success", "data": serializer.data})

   def patch(self, request, pk):
      todo = self.get_todo(pk)
      if todo == None:
         return Response({"status": "fail", "message": f"Todo with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

      serializer = self.serializer_class(todo, data=request.data, partial=True)

      if serializer.is_valid():
         serializer.validated_data['updated_at'] = datetime.now()
         serializer.save()
         return Response({"status": "success", "data": serializer.data})
      return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

   def delete(self, request, pk):
      todo = self.get_todo(pk)
      
      if todo == None:
         return Response({"status": "fail", "message": f"Todo with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
      
      todo.delete()
      return Response({"status": "delete success"})
