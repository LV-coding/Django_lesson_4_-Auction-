from django.urls import path



from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/<int:id>", views.auction_view, name="auction"),
    path("auctions/<int:id>/addcomment", views.add_new_comment, name="addcomment"),
    path("auctions/<int:id>/addbid", views.add_new_bid, name="addbid"),
    path("category", views.all_categories, name="category"),
    path("category/<str:name>", views.choose_category, name="categorysearch"),  
    path("addauction", views.add_new_auction, name="addauction"),
    path("mywatchlist/<int:id>", views.watchlist, name="mywatchlist"),
    path("addtowatchlist/<int:id>", views.add_to_watchlist, name="addtowatchlist"),
    path("changestatus/<int:id>", views.change_status, name="changestatus"),
    path("myauctions/<int:id>", views.myauctions, name="myauctions"),
    path("error", views.forbidden, name="error"),
    path("deactive", views.deactive_auctions, name="deactive"),
]

 
  

 