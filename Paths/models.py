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

class Pathway(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pathway_creator')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
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
        returns True if the previous content is complete and
        """
        print(f"\n\nRUNNING IS_ACTIVE ON {self}")
        print(f"order_position {self.order_position}")
        print(f"pathway content type {self.content_type}")

        if self.order_position > 1:
            previous_content = self.on_pathway.full_pathway.filter(Q(order_position=self.order_position-1))[0]

            # Check whether previous content needs to be completed if not we can pass straight through
            if previous_content.complete_to_move_on:


                # Previous content needs to be completed, lets see if the uSER HAS
                if previous_content.content_type == "article":

                    article_session = ArticleSession.objects.filter((Q(on_article=previous_content.article) & Q(for_user=user))).order_by('-create_date', '-create_time')

                    # If there are sessions there is a possibility to return true
                    if article_session.exists():
                        print("This article has records")
                        print(f"The first in QS: {article_session[0].status} on {article_session[0].create_date}@ {article_session[0].create_time}")
                        print(f"The most last in QS: {article_session[article_session.count()-1].status} on {article_session[article_session.count()-1].create_date}@ {article_session[article_session.count()-1].create_time}")

                        # If the session has been completed or awaiting recap,
                        print(article_session[0].status, type(article_session[0].status))
                        if article_session[0].status == "complete" or article_session[0].status == "recap":
                            print("----------end of article test----------------")
                            return True
                        else:
                            print("----------end of article test----------------")
                            return False
                    # No records have been found, must be false
                    else:
                        print("No records found for this article")
                        print("----------end of article test----------------")
                        return False

                elif previous_content.content_type == "benchmark":
                     benchmark_sessions = BenchmarkSession.objects.filter(Q(on_benchmark=previous_content.benchmark) & Q(for_user=user)).order_by('-create_date', '-create_time')
                     if benchmark_sessions.exists():

                         for benchmark_session in benchmark_sessions:
                            if benchmark_session.session_result >= self.benchmark.percent_to_pass:
                                return True
                         return False

                     else:
                        return False
                elif previous_content.content_type =="video":
                    video_sessions = VideoLectureSession.objects.filter(Q(on_video=previous_content.video)& Q(for_user=user)).order_by('-create_date', '-create_time')
                    if video_sessions.exists():
                        if video_sessions[0].status =="complete" or video_sessions[0].status =="recap":
                            print("----------end of video test----------------")
                            return True
                        else:
                            print("----------end of video test----------------")
                            return False
                    else:
                        print("----------end of video test----------------")
                        return False
                else:
                    print("content type error")

            else:
                print("----------end of complete to move on test----------------")
                return True

        print("----------end of first in position test test----------------")
        return True

class PathwayCompletitionRecord(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_record")
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    pathway_content = models.ForeignKey(PathwayContent, on_delete=models.CASCADE)



class PathwayParticipant(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)#, related_name='pathway_participant')
    on_pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="participants")
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['on_pathway','author'], name="duplicate_pathway_participant")]
