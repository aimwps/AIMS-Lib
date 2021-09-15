from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GeneratedQuestionBank(models.Model):
    SOURCE_TYPE = (("transcript","transcript"),
                            ("literature","literature"),
                            ("document", "document"))
    PROOF_OPTIONS = (("perfect", "perfect"),
                    ("editable", "editable"),
                    ("incorrect","incorrect"),
                    ("unknown", "unknown"))

    generated_date = models.DateField(auto_now_add=True)
    generated_time = models.TimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=255, choices=SOURCE_TYPE)
    source_id = models.PositiveIntegerField()
    question = models.TextField()
    answer = models.TextField()
    user_proof = models.CharField(max_length=255, choices=PROOF_OPTIONS, default="unknown")
