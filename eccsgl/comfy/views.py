from django.shortcuts import render
from comfy.models import Match, User, Team
from django.shortcuts import render_to_response
import datetime
from django.shortcuts import get_object_or_404

# Create your views here.
def all_match_details(request):
    matches = Match.objects.filter(last_updated__gte=datetime.datetime.now()-datetime.timedelta(hours=1)).order_by("state","id")

    match_list = []

    for m in matches:
        m_detail = get_match_dict(m)
        match_list.append(m_detail)

    print(match_list)

    return render_to_response("all_match_data.html",{"match_list" : match_list})

def one_match_details(request,match):
    m = get_object_or_404(Match,pk=match)

    return render_to_response("one_match_detail.html",{"match_dict" : get_match_dict(m) })

def get_match_dict(m):
    m_detail = {"match_id" : m.id,
                    "team_1_name" : m.team_1.name,
                    "team_2_name" : m.team_2.name,
                    "team_1_odds" : m.odds_1,
                    "team_2_odds" : m.odds_2,
                    "time" : m.time,
		    "state" : m.state,
		    "last_updated" : m.last_updated,
		    "winner" : m.winner,
                    }

    return m_detail