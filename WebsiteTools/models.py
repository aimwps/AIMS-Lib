from django.db import models

# Create your models here.
class ContentCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    parent_category = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.SET_NULL)
    global_standard = models.BooleanField(default=False)

    def __str__(self):
        full_path = [self.title]
        k = self.parent_category
        while k is not None:
            full_path.append(k.title)
            k = k.parent_category
        return ' > '.join(full_path[::-1])
