from django.db import models
class RatingField(models.Field):
    "Implements rating system"

    def __init__(self, *args, **kwargs):
        self.score=0
        self.votecount=0
        self.totalscore=0
        super().__init__(*args, **kwargs)
        
    def add(self, score, comment):
        self.totalscore += v
        self.votecount += 1
        self.score = round(self.totalscore/self.votecount, ndigits=2) 