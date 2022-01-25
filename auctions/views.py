from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Auction, User, Comment
import collections
from . import util
from .forms import AuctionForm, AuctionComment
from django.contrib.auth.decorators import login_required

def index(request):
    auction_s = Auction.objects.all()
    auctions = []
    for i in auction_s:
        auctions.append(i)
    auctions.sort (key=lambda auction: auction.created_date, reverse=True)
    categories_list = util.get_category()
    return render(request, "auctions/index.html", {
        "auctions" : auctions,
        "categories_list": categories_list
    })


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


def auction_view(request, id):
    auction = Auction.objects.get(id=id)
    auction_comm = auction.auction_comment.all()
    auction_comment = []
    for i in auction_comm:
        auction_comment.append(i)
    auction_comment.sort (key=lambda comment: comment.created_date_comment, reverse=True)
    return render(request, "auctions/auction.html", {
        "auction" : auction,
        "auction_comment":auction_comment
    })

@login_required
def add_new_comment(request, id):
    auction = Auction.objects.get(id=id)
    if request.method == "POST":
        form = AuctionComment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author_comment = request.user
            new_comment.auction_comment = auction
            new_comment.save()
            return HttpResponseRedirect(reverse("auction", args=(id, )))
    else:
        form = AuctionComment()  
    return render(request, "auctions/addcomment.html", {
        "form":form
    })   

def all_categories(request):
    categories_list = util.get_category()
    return render(request, "auctions/category.html", {
        "categories_list": categories_list
    })


def choose_category(request, name):
    auctions = Auction.objects.all()
    res = []
    for i in auctions:
        if i.category == name:
            res.append(i)
    return render(request, "auctions/categorysearch.html", {
        "auctions": res,
        "name":name
    })


@login_required
def add_new_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form
            auction.instance.author = request.user
            auction.save()
            return HttpResponseRedirect(reverse("index"))
            
    else:
        form = AuctionForm()
    return render(request, "auctions/addauction.html", {
        "form":form
    })