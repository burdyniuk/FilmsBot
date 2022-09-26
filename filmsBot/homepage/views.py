from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("<center><a href='admin'><h1>Admin panel</h1></a></center>")