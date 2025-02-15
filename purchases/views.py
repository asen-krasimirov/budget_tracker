import base64
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import Purchase
from .forms import ImageUploadForm, PurchaseForm
from .utils import save_temp_image, scan_barcode, delete_temp_image


@login_required
def upload_barcode(request):
    """
    Handles barcode image upload, webcam capture, or manual entry.
    """
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        image_path = None
        barcode = None

        if "image" in request.FILES:
            image_path = save_temp_image(request.FILES["image"])

        elif request.POST.get("captured_image"):
            try:
                format, imgstr = request.POST["captured_image"].split(";base64,")
                ext = format.split("/")[-1]
                image_data = ContentFile(base64.b64decode(imgstr), name=f"captured_image.{ext}")
                image_path = save_temp_image(image_data)
            except Exception as e:
                form.add_error(None, "Invalid captured image format.")
                return render(request, "purchases/upload_barcode.html", {"form": form})

        elif request.POST.get("manual_barcode"):
            barcode = request.POST.get("manual_barcode").strip()
            return redirect("add_purchase", barcode=barcode)

        if image_path:
            barcode = scan_barcode(image_path)
            delete_temp_image(image_path)

            if barcode:
                barcode = barcode.decode("utf-8") if isinstance(barcode, bytes) else str(barcode)
                return redirect("add_purchase", barcode=barcode)
            else:
                form.add_error(None, "No barcode detected. Please try again.")

    return render(request, "purchases/upload_barcode.html", {"form": form})


@login_required
def add_purchase(request, barcode):
    """
    Displays product form pre-filled if barcode exists, and saves it if new.
    """
    barcode = barcode.decode("utf-8") if isinstance(barcode, bytes) else str(barcode)
    existing_purchase = Purchase.objects.filter(user=request.user, barcode=barcode).order_by('-date').first()

    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.barcode = barcode
            purchase.save()
            return redirect('dashboard')
    else:
        initial_data = {
            'name': existing_purchase.name if existing_purchase else "",
            'category': existing_purchase.category if existing_purchase else "",
            'price': existing_purchase.price if existing_purchase else "",
        }
        form = PurchaseForm(initial=initial_data)

    return render(request, 'purchases/add_purchase.html', {'form': form, 'barcode': barcode})


@login_required
def delete_purchase(request, purchase_id):
    """
    Deletes a purchase and redirects back to the dashboard.
    """
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    purchase.delete()
    messages.success(request, "Purchase deleted successfully!")
    return redirect("dashboard")


@login_required
def dashboard(request):
    """
    Displays purchases with sorting options.
    """
    sort_by = request.GET.get("sort", "date_desc")
    purchases = Purchase.objects.filter(user=request.user)

    if sort_by == "date_asc":
        purchases = purchases.order_by("date")
    elif sort_by == "date_desc":
        purchases = purchases.order_by("-date")
    elif sort_by == "price_asc":
        purchases = purchases.order_by("price")
    elif sort_by == "price_desc":
        purchases = purchases.order_by("-price")

    return render(request, "purchases/dashboard.html", {"purchases": purchases, "sort_by": sort_by})


@login_required
def export_purchases_csv(request):
    """
    Exports user's purchase data as a CSV file.
    """
    purchases = Purchase.objects.filter(user=request.user)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="purchases.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Product Name", "Price", "Category", "Barcode"])

    for purchase in purchases:
        writer.writerow([purchase.date, purchase.name, purchase.price, purchase.category, purchase.barcode])

    return response
