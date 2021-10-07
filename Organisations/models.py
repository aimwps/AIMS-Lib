from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse
from Paths.models import Pathway
CONTENT_TYPE = (('Pathway', "Pathway"),
                ('Skillset', "Skill-set"),
                )

class Organisation(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="founder")
    members = models.ManyToManyField(User,related_name="group_members")
    create_date = models.DateField(auto_now=False, auto_now_add = True)
    create_time = models.TimeField(auto_now=False, auto_now_add = True)
    parent_organisation = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.SET_NULL)


class OrganisationContent(models.Model):
    assigned_group = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="group_pathways")
    content_type = models.CharField(max_length=100, choices=CONTENT_TYPE)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE)
    #skillset = models.ForeignKey(Pathway, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)