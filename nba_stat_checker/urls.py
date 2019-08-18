from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    re_path(r'^players/(?P<page_letter>[A-Za-z])/(?P<pk>[0-9]+)$',views.PlayerDetailView.as_view(),name='player-detail'),#a page to show individual player details
    re_path(r'^players/(?P<page_letter>[A-Za-z])?$',views.PlayerListView.as_view(),name='players'),# a page to show a list of all players A - Z seperated
    re_path(r'^search/$',views.SearchResultListView.as_view()),
    re_path(r'^teams/$',views.TeamListView.as_view(),name='teams'),
    re_path(r'^teams/(?P<team_name>[A-Za-z]+)/(?P<pk>[0-9]+)$',views.TeamDetailView.as_view(),name='team-detail')
]