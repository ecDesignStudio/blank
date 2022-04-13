from django.shortcuts import render

def home(request):
    context = {}

    return render(request, 'frontend/home.html', context)


