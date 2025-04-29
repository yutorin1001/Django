from django.shortcuts import render, redirect
from .models import Post, Connection,  Reply
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})


@login_required  # ログインしていないユーザーがアクセスできないようにする
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # フォームからインスタンスを作成するが、まだ保存しない
            post.user = request.user        # 現在ログイン中のユーザーを割り当てる
            post.save()                     # インスタンスを保存
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'board/post_list.html', {'form': form})


def post_prof(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/prof.html', {'posts' : posts})
    
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)  # すでに「いいね」している場合は削除
        liked = False
    else:
        post.like.add(request.user)  # 「いいね」を追加
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like.count()})


@login_required
def add_reply(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            reply = Reply.objects.create(post=post, user=request.user, content=content)
            return JsonResponse({
                'success': True,
                'reply': {
                    'user': reply.user.username,  # ユーザー名
                    'content': reply.content,  # 返信内容
                    'created_at': reply.created_at.strftime('%Y-%m-%d %H:%M:%S')  # 作成日時
                }
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})



class DetailPost(LoginRequiredMixin, DetailView):
    """投稿詳細ページ"""
    model = Post
    template_name = 'board/detail.html'  # 使用するテンプレート
    context_object_name = 'post'




def user_profile(request, username):
    # ユーザー情報を取得
    user = get_object_or_404(User, username=username)
    # ユーザーの投稿を取得
    posts = Post.objects.filter(user=user).order_by('-created_at')
    # テンプレートに渡すコンテキスト
    context = {
        'profile_user': user,  # プロフィールのユーザー
        'posts': posts,        # ユーザーの投稿
    }
    return render(request, 'board/profile.html', context)