from django.shortcuts import render , redirect
from .models import *
from django.db.models import Q
from .forms import PostForm, CommentForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm 


# Main Page View

def home(request):

    if request.GET.get('q'):
        posts = Post.objects.filter(topic = request.GET.get('q'))
    elif request.GET.get('search'):
        posts = Post.objects.filter(Q(name__contains = request.GET.get('search')) |
        Q(body__contains = request.GET.get('search')) | 
        Q(tags__name__contains = request.GET.get('search')) )
    else:
        posts = Post.objects.all()


    topics = Topic.objects.all()
    context =  {'topics':topics, 'posts':posts }

    return render(request, 'forum/main.html', context)






def post_page(request,pk):

    post = Post.objects.get(id=pk)
    topics = Topic.objects.all()
    comments = post.comment_set.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))

       
    context = {'post':post, 'comments':comments, 'each_post':True, 'topics':topics , 'form':form}
    return render(request, 'forum/main.html', context)








@login_required
def create_post(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            data = form.save(commit=False)

            data.user = request.user

            form.save()
            return  redirect('home')

    context = {'form':form}
    return render(request,'forum/form_post.html', context)


@login_required
def edit_post(request,pk):
    post = Post.objects.get(id=pk)

    if request.user != post.user:
        return redirect('home')
    
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
 
            form.save()
            return redirect("home")

    context = {'form':form}
    return render(request, 'forum/form_post.html', context)


@login_required
def delete_post(request,pk):
    post = Post.objects.get(id=pk)

    if request.user != post.user:
        return redirect('home')

    post.delete()
    return redirect('home')



def logout_user(request):
    logout(request)
    return redirect('home')




def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            pass

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is Incorrect ! ")

        return redirect('home')





def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.username = user.username.lower()

            form.save()
            login(request, user)

            return redirect('home')

    return render(request, 'forum/register.html')


@login_required
def delete_comment(request,pk):
    comment = Comment.objects.get(id=pk)
    if request.user == comment.user:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def edit_comment(request,post,pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)
    if request.user == comment.user:
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)

            if form.is_valid():
                print("22222222222222222")
                form.save()
                return redirect('post-page', pk=post)
    else:
        return redirect('post-page', pk=post)

    context = {'form':form}

    return render(request, 'forum/edit_comment.html', context)
