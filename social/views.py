from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.models import User, FollowRelation
from .models import Post, Comment, Like
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentForm, CommentReplyForm
from django.db.models import Q
from django.core.paginator import Paginator


class HomeView(View):

    def get(self, request, pnum=1):
        posts = Post.objects.all()
        paginator = Paginator(posts, 3)
        page_number = pnum
        posts = paginator.get_page(page_number)
        return render(request, 'social/home.html', {'posts':posts})


class SearchView(View):

    def get(self, request):
        q = request.GET.get('q')
        if q:
            constraint = Q(body__icontains=q) | Q(title__icontains=q) | Q(user__username__icontains=q)
            posts = Post.objects.filter(constraint)
            paginator = Paginator(posts, 2)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
        return render(request, 'social/home.html', {'posts':posts})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        relation = FollowRelation.objects.filter(follower=request.user.id, followed=user).exists()
        posts = user.posts.all()
        return render(request, 'social/profile.html', {'user':user, 'posts':posts, 'relation':relation})


class FollowingFeedView(LoginRequiredMixin, View):
    def get(self, request):
        relations = request.user.followers.all()
        users = [user.followed for user in relations]
        posts = Post.objects.filter(user__in=users)
        return render(request, 'social/home.html', {'posts':posts})


class PostDetailView(View):
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in', 'danger')
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        like_existance = self.post_instance.like_existance(user=request.user)
        return render(request, 'social/detail.html',
                      {'post':self.post_instance, 'form':form,
                       'reply_form':self.form_class_reply, 'like_existance':like_existance,
                       })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cm = form.save(commit=False)
            cm.user = request.user
            cm.post = self.post_instance
            cm.save()
            messages.success(request, 'comment added successfully', 'success')
            return redirect(self.post_instance.get_absolute_url())
        return render(request, 'social/detail.html', {'post':self.post_instance, 'form':form})


class PostDeleteView(View):

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, slug=kwargs.get('slug'))
        author = self.post.user
        if author != request.user:
            messages.error(request, 'You are not allowed to delete this post', 'danger')
            return redirect(self.post.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        self.post.delete()
        return redirect('social:profile', username=request.user.username)


class PostCreateView(LoginRequiredMixin ,View):
    form_class = PostCreateUpdateForm
    template_name = 'social/create_post.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully', 'success')
            return redirect(post.get_absolute_url())
        return render(request, self.template_name, {'form': form})


class PostUpdateView(LoginRequiredMixin ,View):
    form_class = PostCreateUpdateForm
    template_name = 'social/update_post.html'

    def dispatch(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Post, slug=kwargs.get('slug'))
        author = self.instance.user
        if author != request.user:
            messages.error(request, 'You are not allowed to update this post', 'danger')
            return redirect(self.instance.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        form = self.form_class(instance=self.instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, slug):
        form = self.form_class(request.POST, request.FILES, instance=self.instance)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post updated successfully', 'success')
            return redirect(post.get_absolute_url())
        return render(request, self.template_name, {'form': form})


class CommentReplyView(LoginRequiredMixin , View):
    form_class = CommentReplyForm

    def post(self, request, post_slug, comment_id):
        form = self.form_class(request.POST)
        post_instance = get_object_or_404(Post, slug=post_slug)
        if form.is_valid():
            cm = form.save(commit=False)
            cm.user = request.user
            cm.post = post_instance
            cm.reply = get_object_or_404(Comment, id=comment_id)
            cm.is_reply = True
            cm.save()
            messages.success(request, 'Comment created successfully', 'success')
            return redirect(post_instance.get_absolute_url())
        return render(request, 'social/detail.html', {'form':form})


class LikePostView(LoginRequiredMixin , View):

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.post_instance.user:
            raise ValidationError('You cant like yourself')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        like = Like.objects.filter(user=request.user, post=self.post_instance)
        if not like.exists():
            Like.objects.create(user=request.user, post=self.post_instance)
        else:
            like.delete()
        return redirect(self.post_instance.get_absolute_url())