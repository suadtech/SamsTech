from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')
def test_static_view(request): 
    return render(request, 'test_static.html')