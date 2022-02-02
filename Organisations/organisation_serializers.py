from rest_framework import serializers
from .models import Organisation, OrganisationContent, OrganisationMembers
from Members.members_serializers import UserSerializer
from Paths.pathway_serializers import PathwaySerializer


class OrganisationInfoSearializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
      model = Organisation
      fields = ("author",
                "id",
                "title",
                "description",
                  )

class OrganisationMembersSerializer(serializers.ModelSerializer):
    organisation = OrganisationInfoSearializer()
    member = UserSerializer()
    class Meta:
        model = OrganisationMembers
        fields = ("organisation", "member", "status", "id")

class OrganisationContentSerializer(serializers.ModelSerializer):
    pathway = PathwaySerializer()
    class Meta:
        model = OrganisationContent
        fields = ("pathway",)


class singleOrganisationSerializer(serializers.ModelSerializer):
    org_members = OrganisationMembersSerializer(many=True)
    group_pathways = OrganisationContentSerializer(many=True)
    class Meta:
      model = Organisation
      fields = (
                "id",
                "title",
                "description",
                "org_members",
                "group_pathways",

                  )

class OrganisationSerializer(serializers.ModelSerializer):
    org_members = OrganisationMembersSerializer(many=True)
    group_pathways = OrganisationContentSerializer(many=True)
    parent_organisation = singleOrganisationSerializer()

    class Meta:
      model = Organisation
      fields = ("id",
                "title",
                "description",
                "org_members",
                "group_pathways",
                "parent_organisation"
                  )
