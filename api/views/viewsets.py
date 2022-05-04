from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response



from api.models import Category, Music
from api.serializers import MusicSerializer

import logging
logger = logging.getLogger("django")


class MusicViewSet(viewsets.ViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

    def create(self, request):
        serializer = MusicSerializer(data=request.data)
        logger.info("post {}".format(request.data))        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Music was created"}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        category = request.GET.get('category')
        if category != None:
            self.queryset = Music.manager.get_by_category(category=Category.objects.get(title=category))
        else:
            self.queryset = Music.objects.all()
        serializer = MusicSerializer(self.queryset, many=True)
        return Response({"musics": serializer.data})

    def retrieve(self, request, pk=None):
        music = Music.objects.get(pk=pk)
        serializer = Music(music, many=False)
        
        return Response({"music": serializer.data})
    # @action(methods=['post'], detail=True)
    # def update_(self, request, pk=None):
    #     form = TodoListForm(request.POST, request.FILES)
    #     if form.is_valid() and request.user.is_authenticated:
    #         todoList = TodoList(
    #             id=pk,
    #             owner=request.user,
    #             title=request.POST['title'],
    #             image_file=request.FILES['image_file']
    #         )
    #         todoList.save()
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
