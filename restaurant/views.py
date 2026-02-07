from django.shortcuts import render
from django.utils import timezone
import random
import datetime



RESTAURANT_NAME = "Meizhou Dongpo"



MENU = {
    "dongpo_pork": {"name": "Dongpo Pork (Red-braised pork belly)", "price": 18},
    "mapo_tofu": {"name": "Mapo Tofu", "price": 14},
    "kungpao_chicken": {"name": "Kung Pao Chicken", "price": 16},
    "fried_rice": {"name": "Yangzhou Fried Rice", "price": 9},
    "daily_special": {"name": "Daily Special", "price": 19},
}


DAILY_SPECIALS = [
    "Spicy Szechuan Fish",
    "Mapo Tofu Combo",
    "Dongpo Pork Rice Bowl",
]


def main(request):
    context = {
        "restaurant_name": RESTAURANT_NAME,
        "generated_at": timezone.now(),
    }
    return render(request, "restaurant/main.html", context)


def order(request):
    
    daily_special = random.choice(DAILY_SPECIALS)

    context = {
        "restaurant_name": RESTAURANT_NAME,
        "daily_special": daily_special,
        "generated_at": timezone.now(),
    }
    return render(request, "restaurant/order.html", context)


def confirmation(request):
    
    ordered_ids = request.POST.getlist("items")  

    customer_name = request.POST.get("customer_name", "")
    customer_phone = request.POST.get("customer_phone", "")
    customer_email = request.POST.get("customer_email", "")

    spice_level = request.POST.get("spice_level", "")
    special_instructions = request.POST.get("special_instructions", "")

    
    ordered_items = []
    total = 0.0

    for item_id in ordered_ids:
        if item_id == "daily_special":
           
            daily_name = request.POST.get("daily_special_name", "Daily Special")
            price = MENU["daily_special"]["price"]
            ordered_items.append({"name": daily_name, "price": f"{price:.2f}"})
            total += price
        elif item_id in MENU:
            name = MENU[item_id]["name"]
            price = MENU[item_id]["price"]
            ordered_items.append({"name": name, "price": f"{price:.2f}"})
            total += price

    
    minutes = random.randint(30, 60)
    ready_dt = timezone.localtime(timezone.now()) + datetime.timedelta(minutes=minutes)
    ready_time = ready_dt.strftime("%I:%M %p").lstrip("0")

    context = {
        "restaurant_name": RESTAURANT_NAME,
        "ordered_items": ordered_items,
        "total": f"{total:.2f}",
        "ready_time": ready_time,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "customer_email": customer_email,
        "spice_level": spice_level,
        "special_instructions": special_instructions,
        "generated_at": timezone.now(),
    }

    return render(request, "restaurant/confirmation.html", context)
