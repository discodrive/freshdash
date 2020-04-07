from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from dashboard.models import Client, TimeSheet, ClientOwner, Ticket
from dashboard.forms import LocationFilterForm, OwnerFilterForm


@login_required(login_url='/accounts/login/')
def client(request, clientslug='no-client'):

    client = Client.objects.get(slug=clientslug)
    tickets = client.ticket_set.all()[:3]
    context = {'client': client, 'tickets': tickets}

    return render(request, 'dashboard/client.html', context)

@login_required(login_url='/accounts/login/')
def index(request):
    sort_by = {
        'name' : 'name',
        'time' : 'time_spent',
        'owner' : 'project_owner'
    }

    query = request.GET.dict()
    clients = Client.objects.all().order_by('name')
    owners = ClientOwner.objects.all()

    location_form = LocationFilterForm(request.GET or None)
    owner_form = OwnerFilterForm(
        request.GET or None, 
        initial={'6': 'No owner'}
    )

    if request.method == "GET":
        if location_form.is_valid():
            try:
                if request.GET.get('location'):
                    location = request.GET.get('location')
                    clients = Client.objects.filter(location=location).order_by('name')
            except IntegrityError as e:
                print(e)
        if owner_form.is_valid():
            try:
                if request.GET.get('owner'):
                    owner = request.GET.get('owner')
                    clients = Client.objects.filter(product_owner=owner).order_by('name')
            except IntegrityError as e:
                print(e)

    context = {
        'clients': clients,  
        'owner': owner_form,
        'location': location_form
    }

    return render(request, 'dashboard/index.html', context)

def response(items, failure_message="404 Not found"):
    if items is False:
        raise Http404(failure_message)
    else:
        return JsonResponse(items, safe=False)
