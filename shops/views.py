
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, fromstr
from django.shortcuts import render
from django.views import generic

from .models import Shop

longitude = -80.191788
latitude = 25.761681

user_location = Point(longitude, latitude, srid=4326)


class Home(generic.ListView):
    model = Shop
    context_object_name = 'shops'
    # queryset = Shop.objects.annotate(distance=Distance('location',user_location)).order_by('distance')[0:30]
    template_name = 'shops/index.html'

    def get_queryset(self):
        latitude = self.request.GET.get('latitude')
        longitude = self.request.GET.get('longitude')
        search_radius = self.request.GET.get('search_radius')


        if latitude or longitude:
            longitude = float(longitude)
            latitude = float(latitude)
            search_location = Point(-abs(longitude), latitude, srid=4326)

            return Shop.objects.annotate(distance=Distance('location', search_location)).filter(distance__lte=search_radius*1000).order_by('distance')
            

        # else:
        #     return Shop.objects.annotate(distance=Distance('location',user_location)).order_by('distance')[0:30]
