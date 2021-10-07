from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GeneratedQuestionBank(models.Model):
    SOURCE_TYPE = (("transcript","transcript"),
                            ("article","article"),
                            ("document", "document"))
    PROOF_OPTIONS = (("perfect", "perfect"),
                    ("editable", "editable"),
                    ("incorrect","incorrect"),
                    ("unknown", "unknown"),
                    ("trashed", "trashed"))

    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=255, choices=SOURCE_TYPE)
    source_id = models.PositiveIntegerField()
    question = models.TextField()
    answer = models.TextField()
    user_proof = models.CharField(max_length=255, choices=PROOF_OPTIONS, default="unknown")
