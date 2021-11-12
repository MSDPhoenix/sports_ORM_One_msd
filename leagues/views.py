from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q

from . import team_maker

def index(request):

	current_players_in_the_pacific_basketball_players_association=[]
	for team in Team.objects.filter(league=League.objects.get(name__icontains="pacific basketball players association")):
		for player in team.curr_players.all():
			current_players_in_the_pacific_basketball_players_association.append(player)

	players_in_the_national_federation_of_baseball_named_Ramirez=[]
	teams_in_the_national_federation_of_baseball=Team.objects.filter(league=League.objects.get(name__icontains="national federation of baseball"))
	for team in teams_in_the_national_federation_of_baseball:
		for player in team.curr_players.filter(last_name="Ramirez"):
			players_in_the_national_federation_of_baseball_named_Ramirez.append(player)

	all_football_players=[]
	football_leagues=League.objects.filter(sport__icontains="football")
	for league in football_leagues:
		for team in league.teams.all():
			for player in team.curr_players.all():
				all_football_players.append(player)

	former_players_of_the_Arizona_Bears=[]     # IS THERE A BETTER WAY TO DO THIS?
	all_players_of_the_Arizona_Bears=Team.objects.get(location="Arizona",team_name="Bears").all_players.all()
	current_players_of_the_Arizona_Bears=Team.objects.get(location="Arizona",team_name="Bears").curr_players.all()
	for player in all_players_of_the_Arizona_Bears:
		if player not in current_players_of_the_Arizona_Bears:
			former_players_of_the_Arizona_Bears.append(player)

	Alexander_Landon=Player.objects.get(first_name="Landon",last_name="Alexander") 
	
	players_who_have_played_in_xxxx_league=[]
	
	players_named_Noah_who_have_played_in__the_Pacific_Association_of_Amateur_Football=set(())
	Pacific_Association_of_Amateur_Football=League.objects.get(name="Pacific Association of Amateur Football")
	teams_in_the_Pacific_Association_of_Amateur_Football=Team.objects.filter(league=Pacific_Association_of_Amateur_Football)
	for team in teams_in_the_Pacific_Association_of_Amateur_Football:
		for player in team.all_players.filter(first_name="Noah"):
			players_named_Noah_who_have_played_in__the_Pacific_Association_of_Amateur_Football.add(player)

	teams_that_have_had_12_or_more_players=[]
	for team in Team.objects.all():
		if team.all_players.count()>11:
			teams_that_have_had_12_or_more_players.append(team)

	players_sorted_by_count=[]
	counter=1
	while len(Player.objects.all()) > len(players_sorted_by_count):
		for player in Player.objects.all():
			if player.all_teams.count() == counter:
				players_sorted_by_count.append(player)
		counter+=1
	players_sorted_by_count.reverse()
	
	context = {

		#sports ORM I
		
		"leagues": League.objects.all(),
		"baseball_leagues": League.objects.filter(sport__icontains="baseball"),
		"womens_leagues": League.objects.filter(name__icontains="women"),
		"hockey_leagues": League.objects.filter(sport__icontains="hockey"),
		"non_football_leagues": League.objects.exclude(name__icontains="football"),
		"leagues_that_call_themselves_conferences": League.objects.filter(name__icontains="conference"),
		"leagues_in_the_Pacific_region": League.objects.filter(name__icontains="pacific"),

		"teams": Team.objects.all().order_by("league__id"),
		"teams_based_in_New_Orleans": Team.objects.filter(location__icontains="New Orleans"),
		"teams_named_the_Oilers": Team.objects.filter(team_name__icontains="oilers"),
		"teams_whose_name_includes_blue": Team.objects.filter(team_name__icontains="blue"),
		"teams_whose_names_begin_with_B": Team.objects.filter(team_name__istartswith="b"),
		"teams_ordered_alphabetically_by_location": Team.objects.all().order_by("location"),
		"teams_ordered_by_team_name_in_reverse_alphabetical_order": Team.objects.all().order_by("-team_name"),

		"players": Player.objects.all().order_by("first_name"),
		"players_with_last_name_Gonzalez": Player.objects.filter(last_name="Gonzalez"),
		"players_with_first_name_Jacob": Player.objects.filter(first_name="Jacob"),
		"players_with_last_name_Gonzalez_but_not_first_name_Noah": Player.objects.filter(last_name="Gonzalez").exclude(first_name="Noah"),
		"players_with_first_name_Alexander_or_Wyatt": Player.objects.filter(Q(first_name="Alexander")|Q(first_name="Wyatt")),

		#sports ORM II

		"teams_in_the_pacific_soccer_players_conference": Team.objects.filter(league=League.objects.get(name__icontains="pacific soccer players conference")),
		"current_players_of_the_Florida_Cowboys": Player.objects.filter(curr_team=Team.objects.get(team_name__icontains="Cowboys",location="Florida")),
		"current_players_in_the_pacific_basketball_players_association": current_players_in_the_pacific_basketball_players_association,

		"players_in_the_national_federation_of_baseball_named_Ramirez": players_in_the_national_federation_of_baseball_named_Ramirez,
		"all_football_players": all_football_players,
		"players_named_harper": Player.objects.filter(first_name="Harper"),

		"players_named_Ramirez_who_dont_play_for_the_Miami_Pipers": Player.objects.filter(last_name="Ramirez").exclude(curr_team=Team.objects.get(team_name="Pipers")),
		"teams_that_Jacob_Griffin_has_played_with": Player.objects.get(first_name="Jacob",last_name="Griffin").all_teams.all(),
		"current_and_former_players_of_the_Arizona_Bears": Team.objects.get(location="Arizona",team_name="Bears").all_players.all(),

		"former_players_of_the_Arizona_Bears": former_players_of_the_Arizona_Bears,
		"teams_that_Landon_Alexander_used_to_play_with": Team.objects.filter(all_players=Alexander_Landon).exclude(curr_players=Alexander_Landon),
		"players_named_Noah_who_have_played_in__the_Pacific_Association_of_Amateur_Football": players_named_Noah_who_have_played_in__the_Pacific_Association_of_Amateur_Football,

		"teams_that_have_had_12_or_more_players": teams_that_have_had_12_or_more_players,
		"players_sorted_by_count": players_sorted_by_count,

	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")