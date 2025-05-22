from django.shortcuts import render

# Create your views here.
def index(request):
    
    return render (request, 'app_szulinap/bejelentkezes.html') 

def fooldal(request):
    return render(request, 'app_szulinap/fooldal.html')