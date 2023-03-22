from django.shortcuts import render
from rest_framework import generics
from .models import Team
from .serializers import TeamSerializer


class TeamView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    model = Team
    queryset = Team.objects.all()
