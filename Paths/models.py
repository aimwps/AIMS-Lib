from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from embed_video.fields import EmbedVideoField
from rest_framework import serializers
from VideoLecture.models import VideoLecture, VideoLectureSession
from WrittenLecture.models import Article, ArticleSession
from Benchmark.models import Benchmark, BenchmarkSession
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
PARTICIPATION_STATUS = (
                    ('pending', 'pending'),
                    ('rejected','rejected'),
                    ('active','active'),
                    )


CONTENT_TYPE = (('article', "Article"),
                ('video', "Video"),
                ('benchmark', "Benchmark"),
                )
REVISE_FREQ = ( ('Never', 'Never'),
                ('Daily', 'Daily'),
                ('Weekly', 'Weekly'),
                ('Monthly', 'Monthly'),
                ('Yearly', 'Yearly')
                )
INVITE_TYPES = (
                ("author_free_invite", "author_invite"),
                ("organisation_invite", "organisation_invite"),
                ("author_paid_invite", "author_paid_invite")
                )
MEMBERSHIP_TYPES = (
                ("author_free", "author_invite"),
                ("author_paid", "author_paid_invite"),
                ("organisation_free", "organisation_invite"),
                ("organisation_paid", "organisation_invite"),
                )


class Pathway(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pathway_creator')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500,blank=True)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return f"pathway_{self.id}"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(Pathway, self).get_form_kwargs(
            *args, **kwargs)
        return kwargs

class PathwayCost(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="cost_brackets")
    purchase_quantity = models.PositiveIntegerField()
    purchase_cost = models.DecimalField(decimal_places=2, max_digits=6)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["pathway", "purchase_quantity"], name="duplicate_quantity_costs")]


class PathwayContent(models.Model):
    on_pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name='full_pathway')
    content_type =  models.CharField(max_length=100, choices=CONTENT_TYPE)
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoLecture, blank=True, null=True, on_delete=models.CASCADE)
    benchmark = models.ForeignKey(Benchmark, blank=True, null=True, on_delete=models.CASCADE)
    order_position = models.PositiveIntegerField(default=9999)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)
    complete_to_move_on = models.BooleanField(default=True) #complete_previous
    complete_anytime_overide = models.BooleanField(default=False) #complete_anytime_overide
    revise_frequency = models.CharField(max_length=100, default="Never", choices=REVISE_FREQ)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['on_pathway', 'order_position'],
                name='pathway_order_by'
            )
        ]
        get_latest_by ='order_position'
        ordering = ["order_position"]

    def get_next_order_by(self):
        max_rated_entry = self.objects.latest()
        return int(max_rated_entry.details) + 1
    def pretty_content_type(self):
        pretty_dict = {"written-lecture": "article",
                        "video-lecture": "video",
                        "benchmark": "benchmark",}
        return pretty_dict[self.content_type]

    def is_active(self, user):
        """
        returns True if the previous content is complete or does not need to be completed to unlock the content in question
        """
        if self.order_position > 1:
            previous_content = self.on_pathway.full_pathway.filter(Q(order_position=self.order_position-1))[0]

            # Check whether previous content needs to be completed if not we can pass straight through
            if previous_content.complete_to_move_on:


                # Previous content needs to be completed, lets see if the uSER HAS
                if previous_content.content_type == "article":

                    article_session = ArticleSession.objects.filter((Q(on_article=previous_content.article) & Q(for_user=user))).order_by('-create_date', '-create_time')

                    # If there are sessions there is a possibility to return true
                    if article_session.exists():

                        # If the session has been completed or awaiting recap,

                        if article_session[0].status == "complete" or article_session[0].status == "recap":
                            print("Returned true because user is a member, has sessions as complete or recap")
                            return True
                        else:
                            print("Returned False because user is a member but has NO complete or recap sessions")
                            return False
                    # No records have been found, must be false
                    else:
                        print("returned false because user has NO article session records")
                        return False

                elif previous_content.content_type == "benchmark":

                    benchmark_sessions = BenchmarkSession.objects.filter((Q(on_benchmark=previous_content.benchmark) & Q(for_user=user) & Q(completed=True) )).order_by('-create_date', '-create_time')

                    if benchmark_sessions.exists():
                        for benchmark_session in benchmark_sessions:
                            if benchmark_session.session_result >= previous_content.benchmark.percent_to_pass:
                                return True
                        return False

                    else:

                        return False
                elif previous_content.content_type =="video":
                    video_sessions = VideoLectureSession.objects.filter(Q(on_video=previous_content.video)& Q(for_user=user)).order_by('-create_date', '-create_time')
                    if video_sessions.exists():
                        if video_sessions[0].status =="complete" or video_sessions[0].status =="recap":
                            return True

                        else:

                            return False
                    else:
                        return False
                else:
                    print("content type error")

            else:
                print("returned True because the previous content does not need to be completed")
                return True
        else:
            print("returned true because it's in position 1")
            return True

    def get_latest_result(self, user):
        """
        for a sessions content, see the users latest result.

        For articles and videos this comes in the form of "complete, incomplete, recap or pending"

        For benchmarks this comes in the form of pending or a % result.
        """
        if self.content_type == "article":
            article_session = ArticleSession.objects.filter((Q(on_article=self.article) & Q(for_user=user))).order_by('-create_date', '-create_time')

            # If there are sessions there is a possibility to return true
            if article_session.exists():
                return article_session[0].status
            else:
                return "pending"

        if self.content_type == "benchmark":
            benchmark_sessions = BenchmarkSession.objects.filter((Q(on_benchmark=self.benchmark) & Q(for_user=user) & Q(completed=True) )).order_by('-create_date', '-create_time')

            if benchmark_sessions.exists():
                return f"{benchmark_sessions[0].session_result}%"
            else:
                return "pending"


        if self.content_type == "video":
            video_sessions = VideoLectureSession.objects.filter(Q(on_video=self.video) & Q(for_user=user)).order_by('-create_date', '-create_time')
            if video_sessions.exists():
                return video_sessions[0].status
            else:
                return "pending"



class PathwayParticipant(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)#, related_name='pathway_participant')
    on_pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="participants")
    status = models.CharField(max_length=100, choices=PARTICIPATION_STATUS, default="pending")
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['on_pathway','author'], name="duplicate_pathway_participant")]

class PathwayPurchase(models.Model):
    purchase_type = models.CharField(max_length=100, choices=MEMBERSHIP_TYPES)
    purchase_owner = models.PositiveIntegerField()
    pathway = models.ForeignKey(Pathway, on_delete=models.SET_NULL, null=True)
    spent_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_spends")
    spent_on_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="pathway_purchases")
    status = models.CharField(max_length=100, choices=(("active", "active"), ("pending", "pending"), ("spent", "spent")))
