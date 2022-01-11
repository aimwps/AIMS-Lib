from rest_framework import serializers
from .models import Organisation, OrganisationContent
from Members.members_serializers import UserSerializer
from Paths.pathway_serializers import PathwaySerializer


class OrganisationContentSerializer(serializers.ModelSerializer):
    pathway = PathwaySerializer()
    class Meta:
        model = OrganisationContent
        fields = ("pathway",)


class OrganisationSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    group_pathways = OrganisationContentSerializer(many=True)
    class Meta:
      model = Organisation
      fields = ("members",
                "group_pathways",
                  )
