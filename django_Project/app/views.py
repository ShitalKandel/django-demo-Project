from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hi , There")

# Create your views here.
