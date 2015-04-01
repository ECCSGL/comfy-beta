from django.db import models
import hashlib
import time

def sha256this(string):
    hash = hashlib.sha256()
    hash.update(repr(string).encode("utf-8"))

    return hash.hexdigest()

class User(models.Model):
    hash = models.CharField(max_length=256,default=sha256this(time.time()))
    created = models.DateTimeField()

class Team(models.Model):
    name = models.CharField(max_length=10)

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    team_1 = models.ForeignKey(Team,related_name="matches_as_team_1",null=True)
    team_2 = models.ForeignKey(Team,related_name="matches_as_team_2",null=True)
    odds_1 = models.IntegerField(default=0)
    odds_2 = models.IntegerField(default=0)
    time = models.CharField(max_length=100)

    OPEN = 1
    LIVE = 2
    FINISHED = 3
    PROCESSED = 4
    POSSIBLE_STATES = (
        (OPEN, "Open"),
        (LIVE, "Live"),
        (FINISHED, "Finished"),
        (PROCESSED, "Processed")
    )

    state = models.IntegerField(choices=POSSIBLE_STATES,default=1)
    PENDING = 0
    TEAM_1_WIN = 1
    TEAM_2_WIN = 2
    CLOSED = 3

    POSSIBLE_WINNERS = (
        (PENDING,"Pending"),
        (TEAM_1_WIN, "Team 1"),
        (TEAM_2_WIN, "Team 2"),
        (CLOSED, "Closed/Returned")
    )
    winner = models.IntegerField(choices=POSSIBLE_WINNERS,default=0)

    processed = models.BooleanField(default=False)

    def run_bets(self):
        bets = Bet.objects.filter(match=self)
        print("PROCESSING BETS FOR MATCH ID = {}".format(self.id))
        for bet in bets:
            if self.CLOSED:
                bet.output = bet.amount
                bet.status = bet.CLOSED
            elif self.TEAM_1_WIN and bet.team == 1:
                bet.output = bet.amount + (bet.amount * (self.odds_2 / self.odds_1))
                bet.status = bet.WIN
            elif self.TEAM_2_WIN and bet.team == 2:
                bet.output = bet.amount + (bet.amount * (self.odds_1 / self.odds_2))
                bet.status = bet.WIN
            else:
                bet.status = bet.LOST
            bet.save()
        self.state = self.PROCESSED
        self.save()



class Bet(models.Model):
    match = models.ForeignKey(Match)
    team = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    output = models.FloatField(default=0)

    PENDING = 0
    WON = 1
    LOST = 2
    CLOSED = 3
    BET_STATUSES = (
        (PENDING, "Pending"),
        (WON,"Won"),
        (LOST,"Lost"),
        (CLOSED,"Closed")
    )

    status = models.IntegerField(default=0,choices=BET_STATUSES)