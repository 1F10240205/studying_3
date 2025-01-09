from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, ArticleComment, ArticleContents
from django.contrib.auth import login, logout
from django.http import HttpResponse ,Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = SignupForm()
    
    context = {
        'form': form
    }

    return render(request, 'login_app/signup.html', context)

def login_view(request):
    if request.method == 'POST':
        next = request.POST.get('next')
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                if next == 'None':
                    return redirect(to='main')
                else:
                    return redirect(to=next)
    else:
        form = LoginForm()
        next = request.GET.get('next')

    context = {
        'form': form,
        'next': next
    }

    return render(request, 'login_app/login.html', context)

@login_required
def logout_view(request):
    logout(request)

    return render(request, 'login_app/logout.html')

@login_required
def user_view(request):
    user = request.user

    context = {
        'user': user
    }

    return render(request, 'login_app/user.html', context)

@login_required
def other_view(request):
    users = User.objects.exclude(username=request.user.username)

    context = {
        'users': users
    }

    return render(request, 'login_app/other.html', context)

@login_required
def main_view(request):
    user = request.user
    if request.method == "POST":
        article = ArticleContents(title=request.POST["title"],body=request.POST["text"])
        article.save()
        return redirect(content_view,article.id)

    if ("sort" in request.GET):
        if request.GET["sort"] == "like":
            articles = ArticleContents.objects.order_by("-like")
        else:
            articles = ArticleContents.objects.order_by("-posted_at")
    else:
        articles = ArticleContents.objects.order_by("-posted_at")

    context = {
        "user": user,
		"articles": articles
	}
    return render(request,'login_app/main.html', context)

@login_required
def content_view(request,article_id):
    user = request.user
    try:
        article = ArticleContents.objects.get(pk = article_id)
    except ArticleContents.DoesNotExist:
        raise Http404("Article does not exist")
    
    if request.method == "POST":
        comment = ArticleComment(article = article, text = request.POST["text"])
        comment.save()
    context = {
        'user': user,
        "article":article,
        "comments":article.comments.order_by("-posted_at")
    }
    return render(request,"login_app/content.html",context)
# Create your views here.
