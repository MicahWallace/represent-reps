import re
import urllib2, urllib

from django.utils import simplejson as json

from boundaries.base_views import ModelListView, ModelDetailView, BadRequest
from boundaries.models import Boundary

from representatives.models import (Representative, RepresentativeSet, app_settings,
    Candidate, CandidateSet)
from representatives.utils import boundary_url_to_name

# Oh dear! We're monkey-patching Boundary.as_dict
def boundary_related_decorator(target):
    def inner(self):
        r = target(self)
        r['related']['representatives_url'] = self.get_absolute_url() + 'representatives/'
        return r
    return inner
Boundary.as_dict = boundary_related_decorator(Boundary.as_dict)

class RepresentativeListView(ModelListView):

    model = Representative
    filterable_fields = ('name', 'first_name', 'last_name', 'gender', 'district_name', 'elected_office', 'party_name')
    set_field = 'representative_set'

    def get_qs(self, request, district=None, set_slug=None):
        qs = super(RepresentativeListView, self).get_qs(request)
        if district:
            qs = qs.filter(boundary=district)
        elif set_slug:
            qs = qs.filter(**{self.set_field + '__slug': set_slug})
        return qs

    def filter(self, request, qs):
        qs = super(RepresentativeListView, self).filter(request, qs)

        if 'districts' in request.GET:
            qs = qs.filter(boundary__in=request.GET['districts'].split(','))

        if 'point' in request.GET:
            # Figure out the boundaries for that point
            if app_settings.RESOLVE_POINT_REQUESTS_OVER_HTTP:
                request_url = app_settings.BOUNDARYSERVICE_URL \
                            + 'boundaries/?' + urllib.urlencode({'contains': request.GET['point']})
                resp = urllib2.urlopen(request_url)
                data = json.load(resp)
                boundaries = [ boundary_url_to_name(o['url']) for o in data['objects'] ]
            else:
                try:
                    lat, lon = re.sub(r'[^\d.,-]', '', request.GET['point']).split(',')
                    wkt_pt = 'POINT(%s %s)' % (lon, lat)
                    boundaries = Boundary.objects.filter(shape__contains=wkt_pt).values_list('set_id', 'slug')
                except ValueError:
                    raise BadRequest("Invalid lat/lon values")
                boundaries = ['/'.join(b) for b in boundaries]
            qs = qs.filter(boundary__in=boundaries)

        return qs


class RepresentativeSetListView(ModelListView):

    model = RepresentativeSet
    set_field = 'representative_set'

    def get_qs(self, request):
        qs = super(RepresentativeSetListView, self).get_qs(request)
        return qs.select_related(self.set_field)


class RepresentativeSetDetailView(ModelDetailView):

    model = RepresentativeSet

    def get_object(self, request, qs, slug):
        return qs.get(slug=slug)


class CandidateListView(RepresentativeListView):
    model = Candidate
    set_field = 'candidate_set'


class CandidateSetListView(RepresentativeSetListView):
    model = CandidateSet
    set_field = 'candidate_set'


class CandidateSetDetailView(RepresentativeSetDetailView):
    model = CandidateSet
