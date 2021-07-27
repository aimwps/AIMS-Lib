from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, date
from Development.models import SkillArea, DevelopmentCategory
from ckeditor.fields import RichTextField

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


class VoteUpDown(models.Model):
    votee = models.ForeignKey(User, on_delete=models.CASCADE)
    #on_post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content_type =  models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_up_vote = models.BooleanField()
    objects = VoteManager()

    def __str__(self):
        return f"<VoteUpDown by {self.votee} is_up_vote: {self.is_up_vote}>"



    # def get_absolute_url(self):
    #     return reverse('forum-home')
    #     #return reverse('home')


class CommentManager(models.Manager):
    def filter_by_instance(self,instance):
        obj_id = instance.id
        content_type = ContentType.objects.get_for_model(instance)
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class Post(models.Model):
    title = models.CharField(max_length=255)
    #assigned_skill_area = models.ForeignKey(SkillArea, on_delete=models.CASCADE)
    dev_area = models.ForeignKey(DevelopmentCategory, null=True,on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #body = models.TextField()
    body = RichTextField(blank=True, null=True)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    topic_snippet = models.TextField(max_length=500, default="A short snippet on your topic")
    #modify_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title + ' | ' + str(self.author) #This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #on_post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content_type =  models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    body = models.TextField(max_length=500)
    publish_date = models.DateField(auto_now=False,auto_now_add=True)
    publish_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    objects = CommentManager()




    def __str__(self):
        return "<Comment by " + str(self.author)+">" #This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Post, related_name="replies", on_delete=models.CASCADE)
    #body = models.TextField()
    body = RichTextField(blank=True, null=True)
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)


    def __str__(self):
        return f"<Reply by: {self.author} to: {self.on_post.author} on: {self.publish_date} at: {self.publish_time}>"#This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('forum-home')
        #return reverse('home')
