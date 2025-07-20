from .models import Product
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import requests
# Create your views here.
# products = Product.objects.all()
# laptops = Product.objects.filter(category="Laptop")
# tablets = Product.objects.filter(category="Tablet")
# smartwatches = Product.objects.filter(category="Smartwatch")
# context = {
#     "products": products,
#     "laptops": laptops,
#     "tablets": tablets,
#     "smartwatches": smartwatches,
# }

def home(request):

    # print(context.laptops)
    categories = Product.objects.exclude(category="Laptop").values_list('category', flat=True).distinct()
    categorized_products ={}
    for category in categories: 
        homeProducts = Product.objects.filter(category=category)[:8]
        categorized_products[category] = homeProducts
    laptops = Product.objects.filter(category="Laptop")
    return render(request, 'home.html', {"categorized": categorized_products, "laptops": laptops})

def send_telegram_message(product, phoneNO, product_url=None):
    text = (
        f"New order! \n"
        f"{phoneNO} \n"
        f"Product: {product.prod_name} \n"
        f"price: {product.price}"
    )
    if product_url:
        text += f"Link: {product_url}"
    url= f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    })



def details(request, id):
    product = get_object_or_404(Product, id=id)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    if request.method == "POST":
        phoneNO = request.POST.get("ph_no")
        product_url = request.build_absolute_uri(f"/product/{product.id}")
        send_telegram_message(product, phoneNO, product_url)
        messages.success(request, "Your order has been sent. We will get back to you.")
        return redirect("home")
    return render(request, 'details.html', {"product": product, "similar": similar_products})



def results(request):
    query = request.POST.get("query") or request.GET.get("query", "")
    searches = (Product.objects.filter(Q(prod_name__icontains=query) | Q(category__icontains=query)))
    
    return render(request, 'results.html', {"searches": searches})

def products(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    categorized_products ={}
    for category in categories: 
        products = Product.objects.filter(category=category)[:15]
        categorized_products[category] = products
    return render(request, "products.html", {"products": categorized_products })

def about(request):
    return render(request, "about.html")