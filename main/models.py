from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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

        return obj


    def __str__(self):
        return self.team

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Document(models.Model):
    # content type required context
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    # related model fields
    document = models.FileField(upload_to="docs")
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.document.url

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class UserDocument(models.Model):
    # table for user upload documents
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    qualification_categories = models.CharField(max_length=200) # use the righy field here.

    def __str__(self):
        return self.qualification_categories


class StaffDocument(models.Model):
    uploader = models.ForeignKey(Staff, on_delete=models.CASCADE)
    client_categories = models.CharField(max_length=200) # use the righy field here.

    def __str__(self):
        return self.client_categories


