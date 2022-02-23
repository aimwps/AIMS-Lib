from django.shortcuts import render, get_object_or_404
from .models import VoteContent
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from Paths.models import Pathway
from VideoLecture.models import VideoLecture
from WrittenLecture.models import Article
from Benchmark.models import Benchmark
from Development.models import Aim, Behaviour, StepTracker
from Organisations.models import Organisation
def Vote_ajax_get(request):
    if request.method == "GET":
        return JsonResponse({"up_votes": 5,
                            "down_votes": 3,}, safe=False)
def Vote_ajax_submit(request):
    if request.method == "POST":
        ## Get the data required to vote
        model, content_id  = request.POST.get("content_data").split("_")
        content_type = ContentType.objects.get_for_model(eval(model))
        is_up_vote = request.POST.get("is_up_vote")
        if is_up_vote == "true":
            is_up_vote = True
        else:
            is_up_vote = False

        ## Get the Object to filter votes on
        object = get_object_or_404(eval(model), id=content_id)

        ## Check whether vote already exists
        past_votes = VoteContent.objects.filter_by_instance(object)
        if request.user:
            user_vote = past_votes.filter(author=request.user)
            if user_vote.exists():
                print(user_vote)
                print("User already voted - needs error message")
            else:
                new_vote = VoteContent( author=request.user,
                                        content_type=content_type,
                                        object_id= object.id,
                                        is_up_vote=is_up_vote)
                new_vote.save()
                print("new vote was saved -return messaage to say it was logged")
        else:
            print("user must be logged in to vote")



        #existing_votes = VoteContent.objects.filter_by_instance(object)
    return JsonResponse({"success":"success"}, safe=False)
