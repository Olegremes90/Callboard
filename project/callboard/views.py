from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, User
from .forms import PostForm, CommentForm, AcceptForm
from django.urls import reverse_lazy
from .filters import PostFilter, CommentFilter
from django.views.generic.edit import FormMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.shortcuts import reverse
from django.http import HttpResponse
from django.views import View



class PostList(ListView):
    model = Post
    template_name = 'flatpages/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'flatpages/post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.post_comment = Post.objects.get(id=self.kwargs['pk'])
        form.instance.author_id = User.objects.get(id=self.request.user.id).id
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context['is_not_subscriber'] = self.request.user not in User.objects.filter(groups__name='subscribers')
        print(post)
        context['com'] = Comment.objects.filter(post_comment=post)
        context['posts'] = post.id
        return context


class ProfileView(ListView):
    model = Comment
    template_name = 'flatpages/profile.html'
    context_object_name = 'posts'
    success_url = reverse_lazy('post_comment')
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        qs = Comment.objects.all()
        self.filterset = CommentFilter(self.request.GET, request=self.request, queryset=qs)
        return self.filterset.qs

    def get_context_data (self, **kwargs):
       context = super().get_context_data(**kwargs)
       my_author = User.objects.get(id=self.request.user.id)
       my_post = Post.objects.filter(authors_id=my_author.id)
       context['my_post'] = my_post
       context['filterset'] = self.filterset
       return context




class PostCreate(CreateView):
    permission_required = ('callboard.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_create.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.content_choice='TA'
        post.authors_id = User.objects.get(id=self.request.user.id).id
        form.instance.authors_id = post.authors_id
        return super().form_valid(form)



class PostDelete(DeleteView):
    permission_required = ('callboard.delete_post',)
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')

class CommentDelete(DeleteView):
    model = Comment
    template_name = 'flatpages/comment_delete.html'
    success_url = reverse_lazy('profile')

class PostUpdate(UpdateView):
    permission_required = ('callboard.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_create.html'


class AcceptResponse(UpdateView):
    model = Comment
    form_class = AcceptForm
    template_name = 'flatpages/comment_accept.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context['post'] = post
        return context




    def form_valid(self, form):
       comment = form.save(commit=False)
       comment.author = Comment.objects.get(id=self.kwargs['pk']).author
       comment.text =Comment.objects.get(id=self.kwargs['pk']).text
       return super().form_valid(form)


def subscribe(request):
    user = request.user
    group = Group.objects.get(name='subscribers')
    user.groups.add(group)


    message = 'Вы успешно подписались на рассылку посследних объявлений.'
    return render(request, 'flatpages/subscribe.html',{ 'message': message })
