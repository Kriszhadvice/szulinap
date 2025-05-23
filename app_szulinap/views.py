from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    
    return render (request, 'app_szulinap/bejelentkezes.html') 

def fooldal(request):
    return render(request, 'app_szulinap/fooldal.html')


def ujember(request):
    return render(request, 'app_szulinap/ujember.html')


def feldolgoz(request):
    if request.method != 'POST':
        return HttpResponse('Ez nem post request')
    if 'szoveg' not in request.POST.keys():
        return HttpResponse('nem jött post request')
    

    sorok = request.POST['szoveg'].split('\n')[1:]

    for sor in sorok:
        Ember.letrehozas_sor_alapjan(sor)

    print('Beolvasás vége')
    
    return render (request, 'app_szulinap/kuld.html')