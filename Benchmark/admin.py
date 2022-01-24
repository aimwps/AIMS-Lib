from django.contrib import admin
from .models import Benchmark, Question, Answer, BenchmarkSession, BenchmarkSessionQuestion
# Register your models here.
admin.site.register(Benchmark)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(BenchmarkSession)
admin.site.register(BenchmarkSessionQuestion)
