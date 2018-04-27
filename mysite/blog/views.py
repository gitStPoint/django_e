from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib import admin
# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, '../templates/blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, '../templates/blog/post_detail.html', {'post': post})


class NotLoggedYet(Exception):
    pass


def post_new(request):
    if not request.user.is_authenticated:
        raise NotLoggedYet('''sorry you're not logged yet!
        please login first!''')
    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, '../templates/blog/post_edit.html', {'form': form})


def post_edit(request,pk):
    post = get_object_or_404(Post, pk=pk)

    if not request.user.is_authenticated:
        raise NotLoggedYet('''sorry you're not logged yet!
        please login first!''')
    else:
        if request.method == "POST":
            form = PostForm(request.POST,instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, '../templates/blog/post_edit.html', {'form': form})

