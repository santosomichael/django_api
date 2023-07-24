from django.urls import path
from api.views import TodoList, TodoDetail

urlpatterns = [
    path('', TodoList.as_view()),
    path('<str:pk>', TodoDetail.as_view())
]