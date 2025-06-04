from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from datetime import date, datetime
# Create your views here.
def index(request):
    
    return render (request, 'app_szulinap/bejelentkezes.html') 

def fooldal(request):
    emberek = Ember.objects.all()
    maidatum = date.today()

    def datum_kulonbseg(ember):
        def nap_ev_nelkul(d):
            return date(maidatum.year, d.month, d.day)
        
        szulido = nap_ev_nelkul(ember.szulinap)
        nevnapido = nap_ev_nelkul(ember.nevnap)

        def napok_kulonbseg(d):
            diff = (d - maidatum).days
            return diff if diff >= 0 else diff + 365  

        szulinap_diff = napok_kulonbseg(szulido)
        nevnap_diff = napok_kulonbseg(nevnapido)

        return min(szulinap_diff, nevnap_diff)

    def kozelebbi_datum(ember):
        szuli = date(maidatum.year, ember.szulinap.month, ember.szulinap.day)
        nev = date(maidatum.year, ember.nevnap.month, ember.nevnap.day)
        return szuli if (szuli - maidatum).days % 365 < (nev - maidatum).days % 365 else nev

    emberek = sorted(emberek, key=datum_kulonbseg)

    ember_adatok = []
    for ember in emberek:
        szuli = date(maidatum.year, ember.szulinap.month, ember.szulinap.day)
        nev = date(maidatum.year, ember.nevnap.month, ember.nevnap.day)
        if (szuli - maidatum).days % 365 <= (nev - maidatum).days % 365:
            datum = ember.szulinap.strftime("%m.%d") + " (szülinap)"
        else:
            datum = ember.nevnap.strftime("%m.%d") + " (névnap)"
        ember_adatok.append({
            'id': ember.id,
            'becenev': ember.becenev,
            'datum': datum,
        })

    return render(request, 'app_szulinap/fooldal.html', {
        'emberek': ember_adatok
    })

def ujember(request):
    return render(request, 'app_szulinap/ujember.html')


def kuld(request):
    if request.method != 'POST':
        return HttpResponse('Ez nem post request')
    if 'szoveg' not in request.POST.keys():
        return HttpResponse('nem jött post request')
    

    sorok = request.POST['szoveg'].split('\n')[1:]

    for sor in sorok:
        Ember.letrehozas_sor_alapjan(sor)

    print('Beolvasás vége')
    
    return render (request, 'app_szulinap/kuld.html')

def profil(request, emberid:int):
    ember = Ember.objects.get(id=emberid)
    
    return render(request, 'app_szulinap/profil.html')
