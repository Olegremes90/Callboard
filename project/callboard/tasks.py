from celery import shared_task
from .models import User
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Post
import time


@shared_task
def send_notifications():
    subscribers = set(User.objects.filter(groups__name='subscribers').values_list('email', flat=True))
    pk = Post.objects.latest('id').id
    user = Post.objects.get(id=pk).authors_id
    author = User.objects.get(id=user)
    preview = f'Пользователь {author} добавил новое объявление!'

    title ='Новое обявление'

    user_subscribers = list(User.objects.filter(groups__name='subscribers').values_list(
         'first_name',
          'username',
          'email',
          )
    )
    for first_name, username, email in user_subscribers:
        if not first_name:
            first_name = username

    html_content = render_to_string(
        'registration/post_created_email.html',
        {
            'name': first_name,
            'title': title,
            'text': preview,
            'link': f'{settings.SITE_URL}post/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
