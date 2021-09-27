from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse


class Organisation(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="founder")
    members = models.ManyToManyField(User,related_name="group_members")
    create_date = models.DateField(auto_now=False, auto_now_add = True)
    create_time = models.TimeField(auto_now=False, auto_now_add = True)

class OrganisationSubGroup(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="founder")
    members = models.ManyToManyField(User,related_name="group_members")
    create_date = models.DateField(auto_now=False, auto_now_add = True)
    create_time = models.TimeField(auto_now=False, auto_now_add = True)

    def __str__(self):
        return "".join([c for c in self.name.split() if c != " "]) + "UserGroup"

class OrganisationContentManager(models.Manager):
    def filter_by_instance(self,instance):
        obj_id = instance.id
        content_type = ContentType.objects.get_for_model(instance)
        qs = super(UserCreatedGroupManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class OrganisationContent(models.Model):
    assigned_group = models.ForeignKey(UserCreatedGroup, on_delete=models.CASCADE, related_name="group_pathways")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object =  GenericForeignKey('content_type', 'content_id')
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    objects = UserCreatedGroupManager()
