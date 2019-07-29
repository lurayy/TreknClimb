from django.shortcuts import render
import json
from .models import Trip, TripType
from django.forms.models import model_to_dict


def index(request,package_name = None):
    response = {}
    trips_list = []
    if (package_name):
        triptype = TripType.objects.get(name = str(package_name))
        if triptype:
            trips = Trip.objects.all().filter(type_of_trip = triptype)
            for trip in trips:
                trips_list.append(model_to_dict(trip))
        response['data'] = trips_list
        return render(request, 'package/index.html', response)
    else:
        return render(request, 'package/index.html', response)
