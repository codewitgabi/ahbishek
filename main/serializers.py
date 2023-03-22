from rest_framework.serializers import ModelSerializer
from .models import Team


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = (
                "id",
                "user",
                "team_members",
                "team",
                "description"
                )
        extra_kwargs = {
                "user": {"write_only": True}
                }
