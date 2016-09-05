from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.


@api_view(['GET', 'POST'])
def create(request):
	if request.method == 'POST':
		print (request.data)
	


@api_view(['GET'])
def info(request):
	pass