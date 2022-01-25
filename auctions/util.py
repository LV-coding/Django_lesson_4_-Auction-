from .models import Auction

def get_category():
    categories_list = []
    categories = Auction.objects.all()
    for i in categories:                            # подумати як оптимізувати...
        if i.category not in categories_list:
            categories_list.append(i.category)
    return categories_list