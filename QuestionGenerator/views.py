from django.shortcuts import render
from .models import GeneratedQuestionBank
from WrittenLecture.models import WrittenLecture
from VideoLecture.models import VideoLecture
from .sserializers import GeneratedQuestionBankSerializer
# Create your views here.
def search_questions(request):
    if request.method=="POST":
        search_str = json.loads(request.body).get('searchText')
        written_lecture = WrittenLecture.objects.filter(title__icontains=search_str, author=request.user.id)
        video_lecture = VideoLecture.objects.filter(title__icontains=search_str, author=request.user.id)
        gqb = GeneratedQuestionBank.objects.filter(
                source_id__in=written_lecture, generated_by = request.user.id) | GeneratedQuestionBank.objects.filter(
                source_id__in=written_lecture, generated_by = request.user.id) | GeneratedQuestionBank.objects.filter(
                question__icontains=search_str, generated_by = request.user.id)| GeneratedQuestionBank.objects.filter(
                answer__icontains=search_str, generated_by = request.user.id)
        benchmark_qs = QuizQuestion.objects.filter(on_quiz=json.loads(request.body).get('on_benchmark'))

        new_data = []
        for q in gqb:
            new_data.append(
            {"question":GeneratedQuestionBankSerializer(q).data,
            "benchmark_status":benchmark_qs.filter(generated_from=q.id).exists()})
        print(new_data)
        return JsonResponse(new_data, safe=False)
