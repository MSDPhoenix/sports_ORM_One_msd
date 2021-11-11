from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"baseball_leagues": League.objects.filter(sport__icontains="baseball"),
		"womens_leagues": League.objects.filter(name__icontains="women"),
		"hockey_leagues": League.objects.filter(sport__icontains="hockey"),
		"non_football_leagues": League.objects.exclude(name__icontains="football"),
		"leagues_that_call_themselves_conferences": League.objects.filter(name__icontains="conference"),
		"leagues_in_the_Pacific_region": League.objects.filter(name__icontains="pacific"),

		"teams": Team.objects.all(),
		"teams_based_in_New_Orleans": Team.objects.filter(location__icontains="New Orleans"),
		"teams_named_the_Oilers": Team.objects.filter(team_name__icontains="oilers"),
		"teams_whose_name_includes_blue": Team.objects.filter(team_name__icontains="blue"),
		"teams_whose_names_begin_with_B": Team.objects.filter(team_name__istartswith="b"),
		"teams_ordered_alphabetically_by_location": Team.objects.all().order_by("location"),
		"teams_ordered_by_team_name_in_reverse_alphabetical_order": Team.objects.all().order_by("-team_name"),

		"players": Player.objects.all().order_by('first_name'),
		"players_with_last_name_Gonzalez": Player.objects.filter(last_name="Gonzalez"),
		"players_with_first_name_Jacob": Player.objects.filter(first_name="Jacob"),
		"players_with_last_name_Gonzalez_but_not_first_name_Noah": Player.objects.filter(last_name="Gonzalez").exclude(first_name="Noah"),
		"players_with_first_name_Alexander_or_Wyatt": Player.objects.filter(Q(first_name="Alexander")|Q(first_name="Wyatt")),
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")