from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
# https://docs.djangoproject.com/en/3.2/topics/db/sql/ => conver to sql statement


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def taskList(request):
    # sql = '''select * from api_task order by id DESC'''
    # tasks = Task.objects.raw(sql)
    tasks = Task.objects.all().order_by('id')
    # The negative sign in front of "-id" indicates descending order
    serializer = TaskSerializer(tasks, many=True)
    data = (serializer.data)
    return Response(data)


@api_view(['GET'])
def taskDetail(request, pk):
    # sql = 'select * from api_task WHERE id = %s', [pk]
    # tasks = Task.objects.raw('select * from api_task WHERE id=%s', [pk])
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response('Item succsesfully delete!')
