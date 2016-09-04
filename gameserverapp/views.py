from django.shortcuts import render

# Create your views here.

class GameServerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing game instance
    """
    