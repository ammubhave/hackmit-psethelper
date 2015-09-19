from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    #raise Exception(str(request.META))
    return render_to_response('index.html' , {'user': request.user})

def search(request, class):
    return render_to_response('search.html', {'user': request.user})
