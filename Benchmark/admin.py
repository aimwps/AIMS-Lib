from django.contrib import admin
from .models import Benchmark, Question, Answer
# Register your models here.
admin.site.register(Benchmark)
admin.site.register(Question)
admin.site.register(Answer)
