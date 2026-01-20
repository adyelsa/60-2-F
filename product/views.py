from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Post, Category, Tag
from .forms import PostForm


def index(request):
    return render(request, "index.html")


def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    q = request.GET.get("q")
    category_id = request.GET.get("category")
    selected_tags = request.GET.getlist("tags")
    sort = request.GET.get("sort")

    
    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    
    if category_id:
        posts = posts.filter(category_id=category_id)

    
    if selected_tags:
        posts = posts.filter(tags__id__in=selected_tags).distinct()

    
    if sort == "new":
        posts = posts.order_by("-created_at")
    elif sort == "old":
        posts = posts.order_by("created_at")

    
    paginator = Paginator(posts, 1)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "q": q,
        "categories": categories,
        "selected_category": category_id,
        "tags": tags,
        "selected_tags": selected_tags,
        "sort": sort,
    }

    return render(request, "posts/list.html", context)


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
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})




