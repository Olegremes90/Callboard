from django.db.models.signals import post_save
from django.dispatch import receiver
from callboard.models import Comment, Post, User



#def add_user_author(request):
 #   user = request.user
  #  author = Author.objects.all()
   # user_author = author.add(user)
    #return user_author



#@receiver(post_save, sender=User)
#def add_author(sender, instance, created, **kwargs):
 #   if instance.is_authenticated:
  #      add_user_author