from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, User, Author
from .forms import PostForm, CommentForm, AcceptForm
from django.urls import reverse_lazy
from .filters import PostFilter, CommentFilter

from django.shortcuts import   reverse


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

class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        print(post)
        context['com'] = Comment.objects.filter(post_comment=post)
        context['posts'] = post.id
        return context






class CommentCreate(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'flatpages/create_comment.html'
    success_url = reverse_lazy('post_comment')
#
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_comment = Post.objects.get(id=self.kwargs['pk'])
        form.instance.post = comment.post_comment
        comment.author_id = User.objects.get(id=self.request.user.id).id
        form.instance.author_id = comment.author_id
        comment.status = True
        form.instance.status = comment.status
        print(comment.author_id)
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("post_detail", kwargs={"pk": pk})



class ProfileView(ListView):
    model = Comment
    template_name = 'flatpages/profile.html'
    context_object_name = 'posts'
    success_url = reverse_lazy('post_comment')

    def get_queryset(self):
        queryset = super().get_queryset()
        qs = Comment.objects.all()
        self.filterset = CommentFilter(self.request.GET, request=self.request, queryset=qs)
        print(self.filterset)
        return self.filterset.qs

    def get_context_data (self, **kwargs):
       context = super().get_context_data(**kwargs)
       my_author = Author.objects.get(user_id=self.request.user.id)
       print(my_author)
       print(my_author.id)
       my_post = Post.objects.filter(authors_id=my_author.id)
       print(self.request.user.id)
       print(my_post)
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
        post.authors_id = Author.objects.get(user_id=self.request.user.id).id
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

