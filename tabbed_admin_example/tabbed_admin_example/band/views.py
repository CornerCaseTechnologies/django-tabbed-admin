import json
from django.shortcuts import render
from .models import *

def index(request):
    print(dir(request))
    bands = list(Band.objects.all().values())
    musicians = list(Musician.objects.all().values())

    context = {}
    # context["items"] = items
    context["bands_json"] = json.dumps(bands)
    context["musicians_json"] = json.dumps(musicians)

    return render(request, 'list.html', context)
    # return HttpResponse()