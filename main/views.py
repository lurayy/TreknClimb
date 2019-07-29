from django.shortcuts import render
import json
from package.models import TripType
from django.http import HttpResponse


def index(request):
    if request.method == "POST": 
        triptypes = TripType.objects.all()
        response_json = []
        for trip in triptypes:
            response_json.append(str(trip.name))
        return HttpResponse(json.dumps(response_json), content_type = 'application/json')	
    else:
        return render(request,'main/index.html')
