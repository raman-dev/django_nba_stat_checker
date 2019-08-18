from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Player,PlayerGeneralStatRecord,Team
from django.views import generic
from .forms import SearchForm
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    #number of players 
    num_players = Player.objects.all().count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_players':num_players,
        'num_visits':num_visits,
        'form':SearchForm()
    }
    #render a page with the context data using index.html as a template
    #render function will look in the templates folder of this app if not found will
    #throw an error
    return render(request, 'nba_stat_checker/index.html',context=context)

class TeamListView(generic.ListView):
    model = Team

    def get_context_data(self,**kwargs):
        context = super(TeamListView,self).get_context_data(**kwargs)
        teams = Team.objects.all()
        context['team_list'] = [teams[0:6],teams[6:12],teams[12:18],teams[18:24],teams[24:30]]
        context['form'] = SearchForm()
        return context

class TeamDetailView(generic.DetailView):
    model = Team
    
    def get_context_data(self,**kwargs):
        context = super(TeamDetailView,self).get_context_data(**kwargs)
        player_list = Player.objects.filter(team__team_abbreviation=self.kwargs['team_name'])
        player_cols = []

        length = len(player_list)
        players_per_row = 3
        n = length//players_per_row
        i = 0

        while i < n:
            player_cols.append(player_list[i*players_per_row:(i + 1)*players_per_row])
            i+=1
            
        player_cols.append(player_list[i*players_per_row:])
        context['player_cols'] = player_cols#[player_list[0:third],player_list[third:third*2],player_list[third*2:]]
        context['form'] = SearchForm()
        return context
        
class SearchResultListView(generic.ListView):
    model = Player
    paginate_by=20
    def get_queryset(self):
        form = SearchForm(self.request.GET)
        #on click search what happens?
        #browser sends get request with search string="some_str"
        #here i send the request to the form 
        #form handles data transformatino bla bla bla
        #first get queryset is called
        #when a search is done
        #so first check if the request .session has a previous search
        last_search = self.request.session.get('last_search','')#returns empty if no search exists
        if form.is_valid():
            self.request.session['last_search'] = form.cleaned_data['search']
        return Player.objects.filter(full_name__icontains=self.request.session['last_search'])
    def get_context_data(self,**kwargs):
        context = super(SearchResultListView,self).get_context_data(**kwargs)
        #here return a search string if one exists else don't
        last_search = self.request.session.get('last_search','')
        context['form'] = SearchForm({'search':last_search})
        return context

class PlayerListView(generic.ListView):
    model = Player
    #context_object_name = 'player_list' #name for the list as a template variable
    #queryset = Player.objects.filter(last_name__icontains='james')[:10]#get 10 players that have the string james in them
    #for the above line you can also override the class method get_queryset(self)
    #"""
    paginate_by=30
    def get_queryset(self):
        return Player.objects.filter(last_name__startswith=(self.kwargs['page_letter']).upper())#now letter should be a variable and should change depending on what the user clicks
    #"""
    
    def get_context_data(self,**kwargs):
        context = super(PlayerListView,self).get_context_data(**kwargs)
        context['letter_list'] = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        context['form'] = SearchForm()
        return context

class PlayerDetailView(generic.DetailView):
    model = Player

    def get_context_data(self,**kwargs):
        context = super(PlayerDetailView,self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context