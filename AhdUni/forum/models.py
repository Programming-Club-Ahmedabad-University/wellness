from django.db import models

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):

    title = models.CharField(max_length=256, blank=False)
    text = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    video = models.FileField(null=True, blank = True, upload_to='videos')
    image = models.FileField(null=True, blank = True, upload_to='images')
    status = models.IntegerField(choices=STATUS,default=0)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


