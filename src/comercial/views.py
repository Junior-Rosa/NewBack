from django.shortcuts import render, HttpResponse

# Create your views here.



def index(request):
    """
    Render the index page for the Comercial app.
    """
    return HttpResponse("Comercial app index page")