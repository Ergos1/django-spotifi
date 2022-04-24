
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer

import logging

logger = logging.getLogger(__name__)

@api_view(["GET"])
def check(request):
    if request.method == 'GET':
        return Response(data="message", status=200)

@api_view(["POST"])
def sign_up_user(request):
    if request.method == 'POST':
        logger.debug("data=", request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User was created"}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

