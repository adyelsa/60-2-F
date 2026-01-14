from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm


from .models import Post


from .forms import PostForm



def index(request):
    return render(request, "index.html")

def post_list(request):
    posts = Post.objects.all()

    return render(request, "posts/list.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, "posts/detail.html", {"post": post})

def create_post(request):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, "posts/create.html", {"form": form})


def signup(request):
    if request.method == "POST":

        form = UserCreationForm(request.POST)
        if form.is_valid():

            form.save()

            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


