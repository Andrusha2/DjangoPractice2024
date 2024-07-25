from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.published.all()
    return render(request,
                 'blog/post/list.html',
                 {'posts': posts, 'section': 'list'})


def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_create(request):
    if not request.user.is_authenticated:
        return redirect("account:user_login")
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = Post.Status.PUBLISHED
            post.save()
            return redirect("blog:post_list")
    else:
        form = PostForm()
    return render(request, 'blog/post/create.html', {'form': form})
