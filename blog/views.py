from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Post
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.published.all()
    return render(request,
                 'blog/post/list.html',
                 {'posts': posts, 'section': 'list'})


def post_detail(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.email = request.user.email
        comment.name = request.user.first_name
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)
