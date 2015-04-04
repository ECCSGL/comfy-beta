from django.shortcuts import render
from comfy.models import Match, User, Team, Bet
from django.shortcuts import render_to_response
import datetime
from django.shortcuts import get_object_or_404, redirect
import time
import hashlib

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

    user, user_exists = get_user_details(request)

    response_dict = {"match_dict" : get_match_dict(m) }

    if user_exists:
        try:
            bet = Bet.objects.get(user=user,match=m)
            bet_placed = True
        except:
            bet = None
            bet_placed = False

    response_dict["bet_placed"] = bet_placed
    response_dict["bet"] = bet

    return render_to_response("one_match_detail.html",response_dict)

def account_incl_hash(request,hash):
    user, user_exists = get_user_details(request, hash=hash)
    if not user_exists:
        return account_excl_hash(request)
    bet_history = Bet.objects.filter(user=user).order_by("date_made")[:50]
    response = render_to_response("account_page.html",{"account" : user, "bet_history" : bet_history})
    response.set_cookie("hash",value=hash)
    return response

def account_excl_hash(request):
    user, user_exists = get_user_details(request)
    if user_exists:
        return redirect("comfy.views.account_incl_hash",hash=user.hash)
    user = User.objects.create(hash=sha256this(time.time()))
    user.save()
    return redirect("comfy.views.account_incl_hash",hash=user.hash)

#Helper functions
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

def get_user_details(request, hash=None):
    if hash is None and "hash" in request.COOKIES:
        hash = request.COOKIES["hash"]
    try:
        user = User.objects.get(pk=hash)
        user_exists = True
    except User.DoesNotExist:
        user = None
        user_exists = False
    return user, user_exists

def sha256this(string):
    hash = hashlib.sha256()
    hash.update(repr(string).encode("utf-8"))

    return hash.hexdigest()