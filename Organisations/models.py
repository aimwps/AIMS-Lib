from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse
from Paths.models import Pathway
from django.db.models import Q
CONTENT_TYPE = (('Pathway', "Pathway"),
                ('Skillset', "Skill-set"),
                )
MEMBERSHIP_STATUS = (
                    ('pending', 'pending'),
                    ('rejected','rejected'),
                    ('active','active'),
                    )


class Organisation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="founder")
    create_date = models.DateField(auto_now=False, auto_now_add = True)
    create_time = models.TimeField(auto_now=False, auto_now_add = True)
    parent_organisation = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.SET_NULL)
    force_parent_member = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}_#{self.id}"

    def find_root_organisation(self):
        node = self
        while node.parent_organisation:
            node = node.parent_organisation
        return node

    def is_root(self):
        if self.parent_organisation:
            return False
        else:
            return True



class OrganisationContent(models.Model):
    assigned_group = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="group_pathways")
    content_type = models.CharField(max_length=100, choices=CONTENT_TYPE)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE)
    #skillset = models.ForeignKey(Pathway, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)

class OrganisationMembers(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="org_members")
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=MEMBERSHIP_STATUS)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)


class OrganisationContentTracking(models.Model):
    tracked_by = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='pathway_trackers')
    participants = models.ManyToManyField(User, related_name='tracker_participants')
    on_content = models.ForeignKey(OrganisationContent, on_delete=models.CASCADE, related_name="tracked_content")
