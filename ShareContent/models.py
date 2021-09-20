from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse

class UserCreatedGroup(models.Model):
    name = models.CharField(max_length=255)
    founder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="founder")
    members = models.ManyToManyField(User,related_name="group_members")
    created_date = models.DateField(auto_now=False, auto_now_add = True)
    created_time = models.TimeField(auto_now=False, auto_now_add = True)

    def __str__(self):
        return "".join([c for c in self.name.split() if c != " "]) + "UserGroup"

class UserCreatedGroupManager(models.Manager):
    def filter_by_instance(self,instance):
        obj_id = instance.id
        content_type = ContentType.objects.get_for_model(instance)
        qs = super(UserCreatedGroupManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs



class UserCreatedGroupContent(models.Model):
    assigned_group = models.ForeignKey(UserCreatedGroup, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object =  GenericForeignKey('content_type', 'content_id')
    date_added_to_group = models.DateField(auto_now=False,auto_now_add=True)
    time_added_to_group = models.TimeField(auto_now=False,auto_now_add=True)
    objects = UserCreatedGroupManager()
