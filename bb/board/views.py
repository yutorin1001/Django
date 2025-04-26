from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'board/post_list.html', {'form': form})


def post_prof(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/prof.html', {'posts' : posts})
    

