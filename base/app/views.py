from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import client_serializer, project_serializer, user_serializer
from .models import Client_model, Project_model
from django.contrib.auth.models import User


@api_view(['GET','POST'])
def test(request):
    if request.method == 'GET':
        users = User.objects.all()
        serialized = user_serializer(users, many=True)
        print(serialized.data)
    if request.method == 'POST':
        serialized = user_serializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response('User Created')
    return Response("failed")

@api_view(['GET','POST'])
def client_get_post(request):
    if request.method == 'GET':
        clients = Client_model.objects.all()
        serialized = client_serializer(clients, many=True)

        if serialized.data:
            response_data_list = []
            for client, item in zip(clients, serialized.data):
                client_user = client.created_by
                response_data_list.append({
                    'id' : item['id'],
                    'client_name': item['client_name'],
                    'created_at': item['created_at'],
                    'created_by_user': client_user.username,
                })
            return Response(response_data_list)
        else:
            return Response({})
    if request.method == 'POST':
        serialized = client_serializer(data=request.data)
        #response_data = {}
        if serialized.is_valid():
            client_instance = serialized.save(created_by=request.user)
            response_data = {
                'id': client_instance.id,
                'client_name': client_instance.client_name,
                'created_at': client_instance.created_at,
                'created_by': client_instance.created_by.username
            }
            return Response(response_data)



@api_view(['GET', 'PUT', 'DELETE'])
def client_get_put_delete(request, id):
    client_detail = get_object_or_404(Client_model, pk=id)
    if request.method == 'GET':
        client_serialized = client_serializer(client_detail)
        projects = Project_model.objects.filter(client=client_detail)
        response_data = {
            'id': client_serialized.data['id'],
            'client_name': client_serialized.data['client_name'],
            'projects': [],
            'created_ay': client_serialized.data['created_at'],
            'created_by_user': client_detail.created_by.username,
            'updated_at': client_serialized.data['updated_at'],
        }
        for project in projects:
            response_data['projects'].append({
                'project_name': project.project_name,
                'created_by': project.created_by.username  # You might want to add more fields as needed
            })
        return Response(response_data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serialized = client_serializer(client_detail, data=request.data)
        if serialized.is_valid():
            serialized.save()
            response_data = {
                'id': serialized.data['id'],
                'client_name': serialized.data['client_name'],
                'created_at': serialized.data['created_at'],
                'created_by': client_detail.created_by.username,
                'updated_at': client_detail.updated_at
            }
            return Response(response_data)
    if request.method == 'DELETE':
        client_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_project(request, id):
    client = Client_model.objects.get(pk=id)
    user_list = []
    for item in request.data['users']:
        user_list.append(item['id'])
    request_data = {
        'project_name': request.data['project_name'],
        'client' : client.id,
        'users': user_list,
        'created_by': request.user.id
    }
    serialized = project_serializer(data=request_data)
    if serialized.is_valid():
        serialized.save()
        user_data = User.objects.filter(pk__in= serialized.data['users'])
        user_serialized = user_serializer(user_data, many=True).data
        user_list = []
        for item in user_serialized:
            user_list.append(item)

        response_data = {
            'id': serialized.data['id'],
            'project_name': serialized.data['project_name'],
            'client': client.client_name,
            'users': user_list,
            'created_at': serialized.data['created_at'],
            'created_by': request.user.username
        }

    return Response(response_data)



@api_view(['GET'])
def projects(request):
    project_detail = Project_model.objects.filter(users=request.user)
    serialized = project_serializer(project_detail, many=True)
    response_data_list = []
    if serialized.data:
        for item,project in zip(serialized.data, project_detail):
            project_user = project.created_by
            response_data = {
                'id':item['id'],
                'Project_name': item['project_name'],
                'created_at': item['created_at'],
                'created_by_name': project_user.username,
            }
            response_data_list.append(response_data)
        return Response(response_data_list)
    return Response('No projects')


