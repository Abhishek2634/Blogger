from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_author()

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Post.objects.filter(status='PUB').order_by('-created_at')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self):
        obj = super().get_object()
        Post.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        return obj

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if 'like' in request.POST:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
        if 'comment' in request.POST:
            Comment.objects.create(post=post, author=request.user, text=request.POST.get('text'))
        return redirect('post-detail', pk=post.pk)

class PostCreateView(AuthorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/'
    
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

class PostDeleteView(AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    def get_queryset(self):
        # Allow admin to delete ANY post, but authors only their own
        if self.request.user.is_superuser:
             return self.model.objects.all()
        return self.model.objects.filter(author=self.request.user)
