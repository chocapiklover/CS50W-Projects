from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation


from .models import User, listings, Category, Comments


def index(request):
  
    # get all the active listings
        active_listings = listings.objects.all()
        categoryList = Category.objects.all()
        return render(request, 'auctions/index.html', {
            'active_listings': active_listings,
            'categories': categoryList
            })

def bid(request, listing_id):
    if request.method == 'POST':
        bid_amount = Decimal(request.POST.get('bid_amount'))
        listings_instance = get_object_or_404(listings, pk=listing_id)

        if not listings_instance.status:
            message = 'Bidding is closed for this listing.'
            return render(request, 'auctions/listingview.html', {
            'message': message,
            'listings': listings_instance
            })

        # Check if bid_amount is greater than starting_bid
        if bid_amount > listings_instance.starting_bid:
            listings_instance.starting_bid = bid_amount
            listings_instance.highest_bidder = request.user
            listings_instance.save()
            message = 'Bid Placed sucessfully.'

            return render(request, 'auctions/listingview.html', {
            'message': message,
            'listings': listings_instance
            })

            # return redirect('listingview', listing_id=listing_id)

        # If bid doesn't meet criteria, show an error
        message = 'Bid must be higher than current bid.'
        return render(request, 'auctions/listingview.html', {
        'message': message,
        'listings': listings_instance
        })

    return redirect('listingview', listing_id=listing_id)

def categoryview(request):
    categoryList = Category.objects.all()
    filtered_active_listings = None

    if request.method == 'POST':
        categoryfromform = request.POST.get('category')
        if categoryfromform:  # Check if category is selected
            try:
                category = Category.objects.get(categoryName=categoryfromform)
                filtered_active_listings = listings.objects.filter(status=True, category=category)
            except Category.DoesNotExist:
                filtered_active_listings = []

    return render(request, 'auctions/category.html', {
        'active_listings': filtered_active_listings,
        'categories': categoryList
    })

def listingview(request, listing_id):
    listing_object = get_object_or_404(listings, pk=listing_id)
    user = request.user if request.user.is_authenticated else None
    comments = Comments.objects.filter(listing=listing_object)
    is_watchlist = False
    has_won = False
    

    if user:
        is_watchlist = user.watchlist.filter(pk=listing_id).exists()

        if listing_object.status is False and user == listing_object.highest_bidder:
            has_won = True

    if request.method == 'POST':
        if 'close_auction' in request.POST:
            # Check if the user is the seller before closing the auction
            if user == listing_object.seller:
                listing_object.status = False
                listing_object.save()

        elif 'addtowatchlist' in request.POST:
            addtowatchlist(request, listing_id)
            if user:
                is_watchlist = user.watchlist.filter(pk=listing_id).exists()

    return render(request, 'auctions/listingview.html', {
        'listings': listing_object,
        'is_watchlist': is_watchlist,
        'user': user,
        'has_won': has_won,
        'comments': comments,
        'add_comment_url': reverse('add_comment', args=[listing_id]),
    })

def add_comment(request, listing_id):
    listing_object = get_object_or_404(listings, pk=listing_id)

    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        comment_text = request.POST.get('comment_text', '')

        if user and comment_text:
            Comments.objects.create(user=user, comments=comment_text, listing=listing_object)

    return redirect('listingview', listing_id=listing_id)

@login_required
def addtowatchlist(request, listing_id):
    user = request.user
    listing = get_object_or_404(listings, pk=listing_id) 

    if user.watchlist.filter(pk=listing.id).exists():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    return redirect('listingview', listing_id = listing_id)

@login_required
def watchlist(request):
    user = request.user
    watchlist_item = user.watchlist.all()

    return render(request, 'auctions/watchlist.html', {
        'watchlist_item': watchlist_item,})


def creatlisting(request):
    if request.method == 'POST':
    
    #getting data from the frontend/forms
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('starting_bid')
        image_url = request.POST.get('imageUrl')
        category_name = request.POST.get('category')
    
    # create a new listing with the given data by defining a new variable
    # and inputing the value recieved from the frontend
    # Check if the category already exists, create it if not
        category, created = Category.objects.get_or_create(categoryName=category_name)

        new_listing = listings(
            title = title,
            description = description,
            starting_bid = float(starting_bid),
            image_url = image_url,
            category = category,
            seller = request.user,)

        new_listing.save()
        return HttpResponseRedirect(reverse("listingview", args=[new_listing.id]))
    
    else: 
        # request.method == 'GET'
        categoryList = Category.objects.all()
        return render(request, "auctions/createnewlisting.html", {
            'categories': categoryList})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


