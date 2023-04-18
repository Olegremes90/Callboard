from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Post, User
from django.core.mail import send_mail


@receiver(post_save, sender=Comment)
def my_handler(sender, instance, created, **kwargs):
    if instance.status:
        mail = instance.author.email
        subject = f'{instance.author} {instance.time_add.strftime("%d %m %Y")}'
        send_mail(
            subject,
            "Здравтсвуйте! Ваш отклик был успешно принят пользователем: " f'{instance.post_comment.authors}'".",
            None,
            [mail],
            fail_silently=False,
        )

    mail = instance.post_comment.authors.email
    subject = f'{instance.post_comment.authors} {instance.time_add.strftime("%d %m %Y")}'
    send_mail(
            subject,
            'Здравтсвуйте! Вы получили новый отклик, войдите и посмотрите!',
            None,
            [mail],
            fail_silently=False,
         )
