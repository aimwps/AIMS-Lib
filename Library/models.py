from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from Paths.models import Pathway
from VideoLecture.models import VideoLecture
from WrittenLecture.models import Article
from Benchmark.models import Benchmark
from Development.models import Aim, Behaviour, StepTracker
from Organisations.models import Organisation
from django.views.generic import View


# Create your models here.
LIBRARY_CONTENT_TYPES = (("Article","Article"),
                        ("VideoLecture","Video"),
                        ("Benchmark","Benchmark"),
                        ("Pathway","Pathway"),
                        ("Organisation","Organisation"),
                        ("Aim","Aim"),
                        ("Behaviour", "Behaviour"),
                        ("StepTracker", "StepTracker"))
class LibraryContentType(models.Model):
    content_type = models.CharField(max_length=100)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['content_type'], name='unique_content_type')
        ]
    def __str__(self):
        return f"LCT_{self.id}_{self.content_type}"



class Bookmark(models.Model):
    for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    content_type = models.CharField(max_length=100, choices=LIBRARY_CONTENT_TYPES)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(VideoLecture, on_delete=models.CASCADE, null=True, blank=True)
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE, null=True, blank=True)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, blank=True)
    aim = models.ForeignKey(Aim, on_delete=models.CASCADE, null=True, blank=True)
    behaviour =  models.ForeignKey(Behaviour, on_delete=models.CASCADE, null=True, blank=True)
    steptracker =  models.ForeignKey(StepTracker, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateField(auto_now=False,auto_now_add=True)
    create_time = models.TimeField(auto_now=False,auto_now_add=True)

    @property
    def bookmarked_object(self):
        if self.content_type == "Article":
            return self.article
        elif self.content_type == "VideoLecture":
            return self.video
        elif self.content_type=="Benchmark":
            return self.benchmark
        elif self.content_type =="Pathway":
            return self.pathway
        elif self.content_type =="Organisation":
            return self.organisation
        elif self.content_type =="Aim":
            return self.aim
        elif self.content_type == "Behaviour":
            return self.video
        elif self.content_type == "StepTracker":
            return self.video
        else:
            return "no_object_found"


class LibraryPermission(models.Model):
    # For Viewing - constraint can't be viewed unless previewewd true
    can_be_previewed = models.BooleanField(default=False)
    can_be_viewed = models.BooleanField(default=False)

    # For Using -  constraint bookmarked has to be true to be able to add to external content
    can_be_bookmarked = models.BooleanField(default=False, )
    can_be_added_to_external_content = models.BooleanField(default=False)

    # For visibility
    author_pathways_hidden = models.BooleanField(default=False)
    author_development_hidden = models.BooleanField(default=True)
