from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie


import json

from .models import User, Post, Follow, Like


# def index(request):
#     posts = Post.objects.all().order_by('-time')
#     paginator = Paginator(posts, 2) #change to 10 before pushing

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, "network/index.html", { 'page_obj': page_obj })


def your_view(request):
    # Add logic to handle your GET and PUT requests (if needed)
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-time')
        
        paginator = Paginator(posts, 10)

        # check to see if the user has liked the posts
        for post in posts:
            post.is_liked_by_user = Like.objects.filter(user=request.user.id, post=post).exists()
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            'page_obj': page_obj,
            'user_id': request.user.id
        })

@login_required
def new_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            content = request.POST.get('content')

            # handling for empty content
            if content:
                Post.objects.create(content=content, creator = user)
            
            else:
                messages.error(request, 'Content cannot be empty.', extra_tags="empty post")


            return redirect('index')

        posts = Post.objects.all()

    return render(request, "network/index.html", { 'posts': posts })

def profile_view(request, user_id):
    # Defining the particular targetted user
    user_profile = get_object_or_404(User, pk=user_id)

    current_user = request.user

    # To only get the posts from the targeted user
    user_posts = Post.objects.filter(creator=user_profile).order_by('-time')

    # defining and retrieving the list from the database
    follower = Follow.objects.filter(follower=user_profile)
    following = Follow.objects.filter(following=user_profile)

    #check to see if the user is already following/existing in the follower list
    #returns True if user is in list 
    is_following = Follow.objects.filter(follower=user_profile, following=current_user).exists()


    #pagination
    paginator = Paginator(user_posts, 10) #change to 10 before pushing

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'network/profile.html', {
        'page_obj': page_obj,
        'follower': follower,
        'following': following,
        'user_profile': user_profile,
        'is_following': is_following,
        'current_user': current_user
    })

@login_required
def follow(request, user_id):
    print("Follow view called")
    user_to_follow = get_object_or_404(User, pk=user_id)
    current_user = request.user
    

    # checking Follow table to see if current user is already following, the user to follow
    if current_user != user_to_follow:
        if not Follow.objects.filter(follower=user_to_follow, following=current_user).exists():
            Follow.objects.create(follower=user_to_follow, following=current_user)
            print("Follow object created successfully")
        else:
            print("Already following the user")
    else:
        print("Current user is the same as the user to follow")

    return redirect('profile', user_id=user_id)


@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, pk=user_id)
    current_user = request.user

    # checking Follow table to see if current user is already following, the user to follow
    if current_user != user_to_unfollow:
        Follow.objects.filter(follower=user_to_unfollow, following=current_user).delete()

    return redirect('profile', user_id=user_id)

@login_required
def following_page(request):
    current_user = request.user

    #get users that current user is following
    following_users = Follow.objects.filter(following = current_user)
    following_users_list = [ follow.follower for follow in following_users ]

    if following_users_list: #check if list is not empty

        posts_from_follow = Post.objects.filter(creator__in = following_users_list).order_by('-time')

        paginator = Paginator(posts_from_follow, 2) #change to 10 before pushing

        # check to see if the user has liked the posts
        for post in posts_from_follow:
            post.is_liked_by_user = Like.objects.filter(user=request.user.id, post=post).exists()
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'network/following.html', {
            'page_obj': page_obj,
            'posts_from_follow': posts_from_follow,
            'user_id': request.user.id
         })
    
    else: 
        return render(request, 'network/following.html', {
        'not_following_message': 'You are currently not following any users.',
})


@require_http_methods(["GET"])
@ensure_csrf_cookie
def get_post(request, post_id):

    #getting the post data from the database
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    likes = Like.objects.filter(post=post)
    
    #sending the post data from backend to frontend
    data = {
        'id': post.id,
        'content': post.content,
        'creator': post.creator.username if post.creator else None,
        'time': post.time.strftime('%Y-%m-%d %H:%M:%S') if post.time else None,
        'user' : user.id,
        'likes': [like.user_id for like in likes],
        # Add other fields as needed
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["PUT"])
def update_post(request, post_id):
    
    print("Update Post View: Start")
    try:
        #geting the post from the database
        post = get_object_or_404(Post, id=post_id)
        
        # Load JSON data from the request body of the frontend
        data = json.loads(request.body.decode('utf-8'))
        edited_content = data.get('edited_content')

        # saving the edited content from the frontend to the database
        if edited_content is not None:
            post.content = edited_content
            post.save()

            # passing the content back to the frontend from db
            response_data = {
                'id': post.id,
                'content': post.content,
                'creator': post.creator.username if post.creator else None,
                'time': post.time.strftime('%Y-%m-%d %H:%M:%S') if post.time else None,
                # Add other fields as needed
            }
            print("Update Post View: Success")
            return JsonResponse(response_data)
        else:
            raise ValueError("Edited content is None.")

    except Exception as e:
        print(f"Update Post View: Error - {e}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

     # check if user has already liked post
    already_liked = Like.objects.filter(user=user, post=post).exists()

    if not already_liked:
        #add user to the like list of the post
        Like.objects.create(user=user, post=post)

    response_data = {
        'already_liked': already_liked,
        'like_count': post.likes.count()
    }
    
    return JsonResponse(response_data)


@login_required
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    #check if user has already liked post
    already_liked = Like.objects.filter(user=user, post=post).exists()

    if already_liked:
        #remove like if user has already liked post
        liked_post = Like.objects.filter(user=user, post=post)
        liked_post.delete()

    response_data = {
        'already_liked': already_liked,
        'like_count': post.likes.count(),
    }

    return JsonResponse(response_data)




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
