from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Purchase
from .forms import ImageUploadForm, PurchaseForm
from .utils import save_temp_image, scan_barcode, delete_temp_image
from .forms import ImageUploadForm

import base64
from django.core.files.base import ContentFile


@login_required
def upload_barcode(request):
    """Handles barcode image upload OR webcam capture."""
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        image_path = None  # Default to no image

        if "image" in request.FILES:  # ✅ If user uploaded an image
            image_path = save_temp_image(request.FILES["image"])

        elif request.POST.get("captured_image"):  # ✅ If user captured an image
            try:
                format, imgstr = request.POST["captured_image"].split(";base64,")
                ext = format.split("/")[-1]  # Extract extension (png/jpg)

                image_data = ContentFile(base64.b64decode(imgstr), name=f"captured_image.{ext}")
                image_path = save_temp_image(image_data)  # Save base64 image

            except Exception as e:
                form.add_error(None, "Invalid captured image format.")
                return render(request, "purchases/upload_barcode.html", {"form": form})

        if image_path:  # ✅ Only process if an image is provided
            barcode = scan_barcode(image_path)
            delete_temp_image(image_path)  # Remove temp image

            if barcode:
                barcode = barcode.decode("utf-8") if isinstance(barcode, bytes) else str(barcode)
                return redirect("add_purchase", barcode=barcode)
            else:
                form.add_error(None, "No barcode detected. Please upload a valid barcode image.")

    return render(request, "purchases/upload_barcode.html", {"form": form})

@login_required
def add_purchase(request, barcode):
    """Displays product form pre-filled if barcode exists, and saves it if new."""
    barcode = barcode.decode("utf-8") if isinstance(barcode, bytes) else str(barcode)

    # Check if the product exists for the user
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
        # Pre-fill with existing product details if available
        initial_data = {
            # 'barcode': barcode,
            'name': existing_purchase.name if existing_purchase else "",
            'category': existing_purchase.category if existing_purchase else "",
            'price': existing_purchase.price if existing_purchase else "",
        }
        form = PurchaseForm(initial=initial_data)

    return render(request, 'purchases/add_purchase.html', {'form': form, 'barcode': barcode})

@login_required
def dashboard(request):
    """Shows only purchases of the logged-in user."""
    purchases = Purchase.objects.filter(user=request.user).order_by('-date')
    return render(request, 'purchases/dashboard.html', {'purchases': purchases})
