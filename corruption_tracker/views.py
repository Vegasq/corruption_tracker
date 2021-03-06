import json

from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from claim.models import Claim


def home(request):
    json_file = open(settings.GEOJSON, encoding='utf8')
    json_data = json.load(json_file)
    # print(json_data)

    polygons_values = Claim.objects.values('polygon_id').\
        annotate(count=Count('polygon_id'))

    polygons_dict = {}
    for values_dict in polygons_values:
        polygons_dict[values_dict['polygon_id']] = values_dict['count']
    # print(polygons_dict)

    for polygon in json_data["features"]:
        polygon['claim_count'] = polygons_dict.get(
            str(polygon["properties"]["ID"]), 0)
        # print(polygons_dict.get(str(polygon["properties"]["ID"]), 0))
        # print(polygon)

    places = [{'data': b['properties']['ID'], 'value': b['properties']['NAME']}
              for b in json_data['features'] if b['properties']['NAME']]

    return render(
        request,
        'home.html',
        {'buildings': mark_safe(json.dumps(json_data)),
         'page': 'home',
         'places': mark_safe(json.dumps(places))})


@login_required
def add_page(request):
    json_file = open(settings.GEOJSON, encoding='utf8')
    json_data = json.load(json_file)
    # print(json_data)

    return render(request, 'add_page.html', {'buildings': mark_safe(json.dumps(json_data)),
                                        'page':'add_page'})


def about(request):    
    return render(request, 'about.html', {'page':'about'})    