from django_filters import FilterSet,  ModelChoiceFilter, CharFilter, ChoiceFilter
from .views import *

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

class PostFilter(FilterSet):
    type_category = ChoiceFilter(
        field_name= 'category_choice',
        choices = CATEGORY,
        label='Категория',
        empty_label='все категории',
    )


    title = CharFilter(
        field_name='title',
        label='название',
    )

    class Meta:
        model = Post
        fields = ['type_category',
                  'title',]


def ourBranches(request):
   if request is None:
        return Post.objects.none()

   author=User.objects.get(id=request.user.id)
   post = author.id
   return Post.objects.filter(authors_id=post)



class CommentFilter(FilterSet):
    post_comment = ModelChoiceFilter(
        field_name= 'post_comment_id',
        queryset = ourBranches,
        label='Объявление',
        empty_label='все объявления',
    )

