from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from Paths.models import Pathway
from VideoLecture.models import VideoLecture
from WrittenLecture.models import Article
from Benchmark.models import Benchmark
from Development.models import Aim
from Organisations.models import Organisation
from django.views.generic import View


# Create your models here.
LIBRARY_CONTENT_TYPES = (("Article","Article"),
                        ("VideoLecture","Video"),
                        ("Benchmark","Benchmark"),
                        ("Pathway","Pathway"),
                        ("Organisation","Organisation"),
                        ("Aim","Aim"))
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
