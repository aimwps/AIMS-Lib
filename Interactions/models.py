from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Development.models import ContentCategory
# Create your models here.
class VoteManager(models.Manager):
    def filter_by_instance(self,instance):
        obj_id = instance.id
        content_type = ContentType.objects.get_for_model(instance)
        qs = super(VoteManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

    def filter_by_instance_vote_counts(self,instance):
        obj_id = instance.id
        content_type = ContentType.objects.get_for_model(instance)
        qs_up = super(VoteManager, self).filter(content_type=content_type, is_up_vote=True, object_id=obj_id)
        qs_down = super(VoteManager, self).filter(content_type=content_type,is_up_vote=False, object_id=obj_id)
        return (len(qs_up), len(qs_down))


class VoteContent(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    is_up_vote = models.BooleanField()
    content_type =  models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = VoteManager()

    def __str__(self):
        return f"ContentVote_{self.id}"

class CommentManager(models.Manager):
    def filter_by_instance(self,instance):
        obj_id = instance.id
        content_type = ContentType.objects.get_for_model(instance)
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class CommentContent(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type =  models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    body = models.TextField(max_length=500)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    objects = CommentManager()

    def __str__(self):
        return f"Comment_{self.id}" #This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')
