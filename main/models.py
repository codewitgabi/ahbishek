from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    user = models.ManyToManyField(User, blank=True)
    team = models.CharField(max_length=30)
    description = models.CharField(max_length=30)

    @property
    def team_members(self):
        users = list(self.user.all().values())
        obj = []
        for user in users:
            d = {}
            d["id"] = user["id"]
            d["username"] = user["username"]

            obj.append(d)

        print(obj)

        return obj


    def __str__(self):
        return self.team
