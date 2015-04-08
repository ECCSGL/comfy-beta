from django.shortcuts import render
from comfy.models import Match, User, Team, Bet
from django.shortcuts import render_to_response
import datetime
from django.shortcuts import get_object_or_404, redirect
import django.http
import time
import hashlib
from django.contrib import messages
from django.template import RequestContext

ERRORS = {
    "bets_closed" : "Sorry, you tried to bet on a game that's already closed.",
    "invalid_amount" : "The amount you tried to bet is not one of our earth numbers.",
    "amount_outofrange" : "The amount you tried to bet must be between $0.04 and $240. CSGL make the rules, not me.",
    "not_enough_funds" : "The amount you tried to bet is more than you have, I'm afraid.",
    "account_required" : "You just tried to do something that you can't do without an account.",
    "switch_no_bet" : "You can't switch when you haven't bet already, you naughty false-POST-request-sending human."
}

# Create your views here.
def all_match_details(request):
    matches = Match.objects.filter(last_updated__gte=datetime.datetime.now()-datetime.timedelta(hours=1)).order_by("state","id")

    match_list = []

    for m in matches:
        m_detail = get_match_dict(m)
        match_list.append(m_detail)
    response_dict = {"match_list" : match_list}

    user, user_exists = get_user_details(request)

    response_dict["account"] = user
    response_dict["account_exists"] = user_exists

    context = RequestContext(request, response_dict)
    return render_to_response("slash_all_matches.html",context)

def faq(request):
    user, user_exists = get_user_details(request)
    response_dict = {"account" : user, "account_exists" : user_exists}
    context = RequestContext(request,response_dict)
    return render_to_response("slash_faq.html",context)

def one_match_details(request,match):
    #toggle off bet features for those without logins
    m = get_object_or_404(Match,pk=match)

    user, user_exists = get_user_details(request)

    response_dict = {"match_dict" : get_match_dict(m) }

    response_dict["account"] = user
    response_dict["account_exists"] = user_exists

    if user_exists:
        try:
            bet = Bet.objects.get(user=user,match=m)
            bet_placed = True
        except:
            bet = None
            bet_placed = False

        response_dict["bet_placed"] = bet_placed
        response_dict["bet"] = bet


    context = RequestContext(request, response_dict)
    return render_to_response("slash_match.html",context)

def account_incl_hash(request,hash):
    user, user_exists = get_user_details(request, hash=hash)
    if not user_exists:
        return account_excl_hash(request)
    bet_history = Bet.objects.filter(user=user).order_by("date_made")[:50]

    response_dict = {"account" : user, "bet_history" : bet_history, "account_exists" : user_exists}

    context = RequestContext(request, response_dict)
    response = render_to_response("slash_account.html",context)
    response.set_cookie("hash",value=hash,max_age=28 * 24 * 60 * 60)
    return response

def account_excl_hash(request):
    user, user_exists = get_user_details(request)
    if user_exists:
        return redirect("comfy.views.account_incl_hash",hash=user.hash)
    user = User.objects.create(hash=sha256this(time.time()))
    user.save()
    return redirect("comfy.views.account_incl_hash",hash=user.hash)

def place_bet(request):
    user, user_exists = get_user_details(request)

    bet_dict = bet_form_processing(request)

    if not user_exists:
        messages.add_message(request,messages.ERROR,"account_required")
        return redirect("comfy.views.one_match_details",match=bet_dict["m_id"])

    if not bet_dict["valid"]:
        messages.add_message(request,messages.ERROR,"invalid_betform")
        return redirect("comfy.views.one_match_details",match=bet_dict["m_id"])

    #Check if bets are still open
    match = Match.objects.get(pk=bet_dict["m_id"])
    try:
        bet = Bet.objects.get(user=user,match=match)
        messages.add_message(request,messages.ERROR,"already_bet")
        return redirect("comfy.views.one_match_details",match=bet_dict["m_id"])
    except:
        pass

    if match.state != 1:
        messages.add_message(request,messages.ERROR,"betting_closed")
        return redirect("comfy.views.one_match_details",match=bet_dict["m_id"])


    if bet_dict["amount"] > user.balance:
        messages.add_message(request,messages.ERROR,"not_enough_funds")
        return redirect("comfy.views.one_match_details",match=bet_dict["m_id"])
    else:
        user.balance -= bet_dict["amount"]

    bet = Bet.objects.create(user=user,match=bet_dict["match"],amount=bet_dict["amount"],team=bet_dict["team"])

    bet.save()

    user.save()

    return redirect("comfy.views.one_match_details",match=bet_dict["m_id"])

def switch_bet(request):
    #needs to check if bets are still open
    user, user_exists = get_user_details(request)

    switch_dict = switch_form_processing(request)

    if not user_exists:
        messages.add_message(request,messages.ERROR,"account_required")
        return redirect("comfy.views.one_match_details",match=switch_dict["m_id"])

    if not switch_dict["valid"]:
        messages.add_message(request,messages.ERROR,"invalid_switchform")
        return redirect("comfy.views.one_match_details",match=switch_dict["m_id"])


    match = Match.objects.get(pk=switch_dict["m_id"])

    try:
        bet = Bet.objects.get(user=user,match=match)
    except:
        messages.add_message(request,messages.ERROR,"bet_notfound")
        return redirect("comfy.views.one_match_details",match=switch_dict["m_id"])

    if match.state != 1:
        messages.add_message(request,messages.ERROR,"betting_closed")
        return redirect("comfy.views.one_match_details",match=switch_dict["m_id"])

    bet.team = switch_dict["team"]
    bet.save()

    user.save()

    return redirect("comfy.views.one_match_details",match=switch_dict["m_id"])

#Helper functions
def switch_form_processing(request):
    return_dict = {"valid" : False, "errors" : []}
    if request.method != "POST":
        return return_dict
    try:
        m_id = int(request.POST.get("match",0))
        return_dict["m_id"] = m_id

        team = int(request.POST.get("team",0))
        return_dict["team"] = team

    except:
        return_dict["errors"].append("")
        return return_dict

    if team is None or m_id is None:
        return_dict["errors"].append("")
        return return_dict

    if team != 1 and team != 2:
        return_dict["errors"].append("")
        return return_dict

    try:
        match = Match.objects.get(pk=m_id)
        return_dict["match"] = match
    except:
        return_dict["errors"].append("")
        return return_dict

    return_dict["valid"] = True
    return return_dict

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

def bet_form_processing(request):
    return_dict = {"valid" : False, "errors" : []}
    if request.method != "POST":
        return return_dict

    try:
        m_id = int(request.POST.get("match",0))
        return_dict["m_id"] = m_id

        team = int(request.POST.get("team",0))
        return_dict["team"] = team


        amount = float(request.POST.get("amount",0))
        return_dict["amount"] = amount

    except:
        return_dict["errors"].append("")
        return return_dict

    if team is None or m_id is None or amount is None:
        return_dict["errors"].append("")
        return return_dict

    if team != 1 and team != 2:
        return_dict["errors"].append("")
        return return_dict

    try:
        match = Match.objects.get(pk=m_id)
        return_dict["match"] = match
    except:
        return_dict["errors"].append("")
        return return_dict

    if amount < 0.04 or amount > 240:
        return_dict["errors"].append("")
        return return_dict

    return_dict["valid"] = True
    return return_dict
