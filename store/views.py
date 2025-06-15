from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def details(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == "POST":
        phoneNO = request.POST.get("ph_no")
        product_name = request.POST.get("product_name")
        product_id = request.POST.get("product_id")

        send_mail(
            subject = "New Order Placed",
            message = f"An order has been placed by the number of {phoneNO} \n Product Name:{product_name}. \n Product ID: {product_id} ",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = ["esakmulushewa@gmail.com"],

            fail_silently = False,
        )
        print("email sent")
    return render(request, 'details.html', {"product": product})

def results(request):
    if request.method == "POST":
        query = request.POST.get("query")
        results = Product.objects.filter(prod_name__icontains=query)
        print(results)
    return render(request, 'results.html', {results: "results"})