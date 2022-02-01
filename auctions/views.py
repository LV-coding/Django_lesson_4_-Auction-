from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Auction, User, Comment, Watchlist, AuctionBid
import collections
from . import util
from .forms import AuctionForm, AuctionComment, AuctionBidForm
from django.contrib.auth.decorators import login_required

def index(request):
    auctions = Auction.objects.all().filter(status=True).order_by('-created_date')
    categories_list = util.get_category()
    return render(request, "auctions/index.html", {
        "auctions" : auctions,
        "categories_list": categories_list
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
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
    auction_comment = auction.auction_comment.all().order_by('-created_date_comment')
    try:
        userwatchlist = Watchlist.objects.filter(author_watchlist=request.user, auctions_list=auction)
    except:
        return HttpResponseRedirect(reverse("index")) 
    flag = False    #for add/delete in watchlist
    for i in userwatchlist:
        if i.auctions_list == auction:
            flag = True
    
    return render(request, "auctions/auction.html", {
        "auction" : auction,
        "auction_comment":auction_comment, 
        "flag": flag
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

@login_required
def add_new_bid(request, id):
    auction = Auction.objects.get(id=id)
    if request.method == "POST":
        form = AuctionBidForm(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            if new_bid.price_bid > auction.price and auction.status == True:
                new_bid.author_bid = request.user
                new_bid.auction_bid = auction
                new_bid.save()
                auction.price = new_bid.price_bid
                auction.save()
                return HttpResponseRedirect(reverse("addbid", args=(id, )))
            else:
                new_bid = ""
                return HttpResponseRedirect(reverse("addbid", args=(id, )))
    else:
        form = AuctionBidForm() 
    allbid = AuctionBid.objects.filter(auction_bid=auction).order_by('-price_bid')
    if allbid:
        current_price = allbid[0]
    else:
        current_price = auction.price
    return render(request, "auctions/addbid.html", {
    "auction":auction,
    "allbid":allbid,
    "form":form,
    "current_price":current_price
    }) 





def all_categories(request):
    categories_list = util.get_category()
    return render(request, "auctions/category.html", {
        "categories_list": categories_list
    })


def choose_category(request, name):
    auctions = Auction.objects.all().filter(status=True)
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
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form
            auction.instance.author = request.user
            auction.save()
            return HttpResponseRedirect(reverse("myauctions", args=(request.user.id,)))
            
    else:
        form = AuctionForm()
    return render(request, "auctions/addauction.html", {
        "form":form
    })

@login_required         
def watchlist(request, id):                           
    searchuser = User.objects.get(id=id)
    userwatchlist = Watchlist.objects.all().filter(author_watchlist=searchuser)
    if id == request.user.id: 
        return render(request, "auctions/mywatchlist.html", {
            "userwatchlist":userwatchlist
        })
    else:
        return HttpResponseRedirect(reverse("error"))

@login_required 
def change_status(request, id):
    auction = Auction.objects.get(id=id)
    if auction.author == request.user:
        if auction.status == True:
            auction.status = False
            auction.save()
        else:
            auction.status = True
            auction.save()  
        return HttpResponseRedirect(reverse("auction", args=(id,)))  
    else:
        return HttpResponseRedirect(reverse("error")) 



@login_required 
def add_to_watchlist(request, id):
    auction = Auction.objects.get(id=id)
    userwatchlist = Watchlist.objects.filter(author_watchlist=request.user, auctions_list=auction)
    flag = False
    for i in userwatchlist:
        if i.auctions_list == auction:
            flag = True
    if not flag:
        forsave = Watchlist(author_watchlist=request.user, auctions_list=auction)
        forsave.save()
    else:
        fordelete = Watchlist.objects.filter(author_watchlist=request.user, auctions_list=auction) 
        fordelete.delete()
    return HttpResponseRedirect(reverse("mywatchlist", args=(request.user.id,)))


@login_required 
def myauctions(request, id):
    us = User.objects.get(id=id)
    auctions = Auction.objects.filter(author=us)
    if request.user.id == id:
        return render(request, "auctions/myauctions.html", {
            "auctions":auctions
        })
    else:
        return HttpResponseRedirect(reverse("error"))

def forbidden(request):
    return render(request, "auctions/error.html")
 

def deactive_auctions(request):
    auctions = Auction.objects.filter(status=False)
    return render(request, "auctions/deactive.html", {
      "auctions":auctions  
    })   


    