"""
views.py
Xinxu Chen (chenxin@bu.edu)

Defines views for voter list, detail page, and graphs.
"""

from urllib.parse import quote_plus

from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.views.generic import DetailView, ListView, TemplateView

import plotly.graph_objs as go
from plotly.offline import plot

from .models import Voter


def get_filtered_queryset(request):
    qs = Voter.objects.all()

    party = request.GET.get('party')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    voter_score = request.GET.get('voter_score')

    if party:
        qs = qs.filter(party_affiliation=party)

    if min_year:
        qs = qs.filter(date_of_birth__year__gte=min_year)

    if max_year:
        qs = qs.filter(date_of_birth__year__lte=max_year)

    if voter_score:
        qs = qs.filter(voter_score=voter_score)

    if request.GET.get('v20state'):
        qs = qs.filter(v20state=True)

    if request.GET.get('v21town'):
        qs = qs.filter(v21town=True)

    if request.GET.get('v21primary'):
        qs = qs.filter(v21primary=True)

    if request.GET.get('v22general'):
        qs = qs.filter(v22general=True)

    if request.GET.get('v23town'):
        qs = qs.filter(v23town=True)

    return qs


def get_common_filter_context(request):
    parties = (
        Voter.objects.exclude(party_affiliation='')
        .values_list('party_affiliation', flat=True)
        .distinct()
        .order_by('party_affiliation')
    )

    years = (
        Voter.objects.exclude(date_of_birth__isnull=True)
        .annotate(year=ExtractYear('date_of_birth'))
        .values_list('year', flat=True)
        .distinct()
        .order_by('year')
    )

    return {
        'parties': parties,
        'years': years,
        'selected_party': request.GET.get('party', ''),
        'selected_min_year': request.GET.get('min_year', ''),
        'selected_max_year': request.GET.get('max_year', ''),
        'selected_voter_score': request.GET.get('voter_score', ''),
        'checked_v20state': request.GET.get('v20state', ''),
        'checked_v21town': request.GET.get('v21town', ''),
        'checked_v21primary': request.GET.get('v21primary', ''),
        'checked_v22general': request.GET.get('v22general', ''),
        'checked_v23town': request.GET.get('v23town', ''),
    }


class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        return get_filtered_queryset(self.request).order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_filter_context(self.request))
        context['result_count'] = self.get_queryset().count()
        context['query_string'] = self.request.GET.copy()
        if 'page' in context['query_string']:
            context['query_string'].pop('page')
        context['query_string'] = context['query_string'].urlencode()
        return context


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_url'] = (
            'https://www.google.com/maps/search/?api=1&query='
            + quote_plus(self.object.full_address())
        )
        return context


class GraphView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        voters = get_filtered_queryset(self.request)
        context.update(get_common_filter_context(self.request))
        context['result_count'] = voters.count()

        year_data = (
            voters.exclude(date_of_birth__isnull=True)
            .annotate(year=ExtractYear('date_of_birth'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        years = [item['year'] for item in year_data]
        year_counts = [item['count'] for item in year_data]

        year_fig = go.Figure(
            data=[go.Bar(x=years, y=year_counts)]
        )
        year_fig.update_layout(
            title='Distribution of Voters by Birth Year',
            xaxis_title='Birth Year',
            yaxis_title='Number of Voters',
        )
        context['birth_year_graph'] = plot(year_fig, output_type='div')

        party_data = (
            voters.exclude(party_affiliation='')
            .values('party_affiliation')
            .annotate(count=Count('id'))
            .order_by('party_affiliation')
        )

        party_labels = [item['party_affiliation'] for item in party_data]
        party_counts = [item['count'] for item in party_data]

        party_fig = go.Figure(
            data=[go.Pie(labels=party_labels, values=party_counts)]
        )
        party_fig.update_layout(
            title='Distribution of Voters by Party Affiliation'
        )
        context['party_graph'] = plot(party_fig, output_type='div')

        election_names = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count(),
        ]

        election_fig = go.Figure(
            data=[go.Bar(x=election_names, y=election_counts)]
        )
        election_fig.update_layout(
            title='Participation in Previous Elections',
            xaxis_title='Election',
            yaxis_title='Number of Voters',
        )
        context['election_graph'] = plot(election_fig, output_type='div')

        return context