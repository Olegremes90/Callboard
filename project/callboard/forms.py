from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
   text = forms.CharField(min_length=20)
   class Meta:
       model = Post
       fields = [
           'category_choice',
           'title',
           #'authors',
           'text',
           'upload',
       ]

   def clean(self):
       cleaned_data = super().clean()
       name = cleaned_data.get('title')
       text = cleaned_data.get("text")
       author = cleaned_data.get('authors')

       if name == text:
           raise ValidationError(
               "Описание не должно быть идентично названию."
           )
       #if author != User.objects.get(id=self.request.user.id):
        #   raise ValidationError(
         #      'Автор указаан не верно.'
          # )

       return cleaned_data


class CommentForm(forms.ModelForm):
   text = forms.CharField(min_length=20, label="Текст")
   class Meta:
         model = Comment
         fields = ['text',
                   ]

   def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('title')
        text = cleaned_data.get("text")
        if name == text:
            raise ValidationError(
                  "Описание не должно быть идентично названию."
          )

class AcceptForm(forms.ModelForm):
    status = forms.BooleanField(label='Принять отклик')
    class Meta:
        model = Comment
        fields = ['status',]

