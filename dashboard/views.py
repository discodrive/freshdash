from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import Client, TimeSheet, ClientOwner, Ticket


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

    if request.GET.get('location'):
        location = request.GET.get('location')
        clients = Client.objects.filter(location=location).order_by('name')
    elif request.GET.get('owner'):
        owner = request.GET.get('owner')
        clients = Client.objects.filter(product_owner=owner).order_by('name')

    # for key, value in sort_by.items():
    #     if query and query['sort'] == key:
    #         clients = clients.order_by(value)
            # clients.sort(key=lambda x: getattr(x, value)())

    context = {'clients': clients,  'owners': owners}

    return render(request, 'dashboard/index.html', context)

def response(items, failure_message="404 Not found"):
    if items is False:
        raise Http404(failure_message)
    else:
        return JsonResponse(items, safe=False)
