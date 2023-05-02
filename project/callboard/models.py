#import tinymce.models
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse




class Post(models.Model):
    CATEGORY = (
        ('TA', 'Танки'),
        ('SI', 'Хиллы'),
        ('DD', 'ДД'),
        ('TR', 'Торговцы'),
        ('GU', 'Гилдмастеры'),
        ('QU', 'Квестгиверы'),
        ('BL', 'Кузнецы'),
        ('SK', 'Кожевники'),
        ('PO', 'Зельевары'),
        ('MA', 'Мастера заклинаний')
    )
    category_choice = models.CharField(max_length=2, choices=CATEGORY, default='TA')
    title = models.CharField(max_length=128)
    text = RichTextField(blank=True, null=True)
    time_creation = models.DateField(auto_now_add=True)
    authors = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = RichTextUploadingField(blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name='subscribe')



    def __str__(self):
        return self.title
# Create your models here.

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    text = models.TextField()
    time_add = models.DateField(auto_now_add=True)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reply')
    author = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.text[0:35] +'...'


    def boolean(self):
        self.status = True
        return self.status