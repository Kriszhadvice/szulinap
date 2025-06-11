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

        szuli_diff = (szuli - maidatum).days if (szuli - maidatum).days >= 0 else (szuli - maidatum).days + 365
        nev_diff = (nev - maidatum).days if (nev - maidatum).days >= 0 else (nev - maidatum).days + 365



        if szuli_diff <= nev_diff:
            datum = ember.szulinap.strftime("%m.%d") + " (szülinap)"
            diff = szuli_diff
        else:
            datum = ember.nevnap.strftime("%m.%d") + " (névnap)"
            diff = nev_diff  
      
        alap = False      
        heti = False
        havi = False
        surgos = False
        if 7 < diff < 31:
            havi = True
        elif ember.ajandek  and diff < 8:
            heti = True   
        elif diff < 8:
            surgos = True 
        else:
            alap = True
        ember_adatok.append({
            'id': ember.id,
            'becenev': ember.becenev,
            'datum': datum,
            'heti': heti,
            'surgos': surgos,
            'havi': havi,
            'alap': alap,
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
    

    sorok = request.POST['szoveg'].split('\n')

    for sor in sorok:
        Ember.letrehozas_sor_alapjan(sor)

    print('Beolvasás vége')
    
    return render (request, 'app_szulinap/kuld.html')

def profil(request, emberid:int):
    
    ember = Ember.objects.get(id=emberid)
    
    context = {
        'szulinap': ember.szulinap.strftime("%m-%d"),
        'nevnap': ember.nevnap.strftime("%m-%d"),
        'ember': ember,
    }
    return render(request, 'app_szulinap/profil.html', context)

def torol(request, emberid:int):
    ember = Ember.objects.get(id=emberid)
    ember.delete()
    return render(request, 'app_szulinap/torol.html')