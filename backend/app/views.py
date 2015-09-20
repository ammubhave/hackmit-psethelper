from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from app.models import Party, PartyRequest
from datetime import datetime
from django.utils import dateparse
from django.shortcuts import redirect

# Create your views here.
@login_required
def home(request):
    #raise Exception(str(request.META))
    return render_to_response('index.html' , {'user': request.user})

@login_required
def search(request):
    q = request.GET['q']
    results = Party.objects.filter(class_for=q, end_datetime__gte=datetime.now())
    return render_to_response('search.html', {'user': request.user, 'q': q, 'results': results})

@login_required
def create(request):
    if request.method == 'GET':
        return render_to_response('create.html', {'user': request.user})
    else:
        class_for = request.POST['class_for']
        short_description = request.POST['short_description']
        description = request.POST['description']
        location = request.POST['location']
        start_datetime = dateparse.parse_datetime(request.POST['start_datetime'])
        end_datetime = dateparse.parse_datetime(request.POST['end_datetime'])
        party = Party.objects.create(organizer=request.user, class_for=class_for, short_description=short_description, decription=description, location=location, start_datetime=start_datetime, end_datetime=end_datetime)
        return redirect('/monitor?id=' + str(party))

@login_required
def monitor(request):
    party = Party.objects.get(id=request.GET['id'], organizer=request.user.username)
    if request.method == 'GET':
        party_requests = PartyRequest.objects.filter(party=party.id).order_by('approved')
        return render_to_response('monitor.html', {'user': request.user, 'party': party, 'party_requests': party_requests})
    else:
        party_request = PartyRequest.objects.get(id=request.POST['request_id'])
        if 'approved' in request.POST:
            party_request.approved = True
            party_request.save()
        return redirect('/monitor?id=' + request.GET['id'])

@login_required
def ask(request):
    party = Party.objects.get(id=request.GET['id'])
    party_request = PartyRequest.objects.filter(party=party.id, requestor=request.user.username)
    if (len(party_request) > 0):
        party_request = party_request[0]
    else:
        party_request = None
    if request.method == 'GET':
        return render_to_response('ask.html', {'user': request.user, 'party': party,'party_request': party_request})
    else:
        if party_request is None:
            party_request = PartyRequest.objects.create(party=party, requestor=request.user)
        return redirect('/ask?id=' + request.GET['id'])

