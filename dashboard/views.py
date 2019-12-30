from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import Client, TimeSheet, ClientOwner


@login_required(login_url='/accounts/login/')
def index(request):
    sort_by = {
        'name' : 'name',
        'time' : 'time_spent',
        'owner' : 'project_owner'
    }

    query = request.GET.dict()
    clients = Client.objects.all()

    for key, value in sort_by.items():
        if query and query['sort'] == key:
            clients = clients.order_by(value)
            # clients.sort(key=lambda x: getattr(x, value)())

    context = {'clients': clients}

    return render(request, 'dashboard/index.html', context)

def response(items, failure_message="404 Not found"):
    if items is False:
        raise Http404(failure_message)
    else:
        return JsonResponse(items, safe=False)
