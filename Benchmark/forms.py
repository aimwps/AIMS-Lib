from django import forms
from .models import Benchmark, Answer, Question
from bootstrap_datepicker_plus import DatePickerInput

class BenchmarkEditAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = (  "answer_text",
                    "is_correct",
                    "is_default",
                )
        widgets = {
            "answer_text":forms.TextInput(attrs = {'class': 'form-control',}),
            "is_correct":forms.Select(attrs = {'class': 'form-control',
                                            }),
            "is_default":forms.Select(attrs = {'class': 'form-control',
                                            }),

            }



class BenchmarkEditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
                "id",
                "question_text",
                "answer_type",
                "order_position",
                )
        widgets = {
                    "id":forms.TextInput(attrs = {'class': 'form-control',
                                                    }),
            "question_text":forms.Textarea(attrs = {'class': 'form-control','rows':3}),
            "answer_type":forms.Select(attrs = {'class': 'form-control',
                                            }),
            "order_position":forms.TextInput(attrs = {'class': 'form-control',
                                            }),
            }
class BenchmarkNewAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = (  "on_question",
                    "generator_source",
                    "source_was_modified",
                    "answer_text",
                    "is_correct",
                    "is_default",
                    )
        widgets ={
            "on_question" : forms.Select(attrs = {'type': 'hidden', 'class': 'form-control',
                                            }),
            "generator_source":forms.Select(attrs = {'type': 'hidden','class': 'form-control',
                                            }) ,
            "source_was_modified":forms.Select(attrs = {'type': 'hidden','class': 'form-control',
                                            }) ,
            "answer_text":forms.TextInput(attrs = {'class': 'form-control',}),
            "is_correct":forms.Select(attrs = {'class': 'form-control',
                                            }),
            "is_default":forms.Select(attrs = {'class': 'form-control',
                                            }),

            }



class BenchmarkNewForm(forms.ModelForm):
    class Meta:
        model = Benchmark
        fields = ('title',)
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'Enter the title of your new benchmark'}),
            }
