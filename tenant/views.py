from django.shortcuts import render

def landing_page(request):
    return render(request, 'tenant/landing.html')


def index(request):
    return render(request, 'tenant/index.html') 
