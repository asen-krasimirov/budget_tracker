from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Purchase
from .forms import ImageUploadForm, PurchaseForm
from .utils import save_temp_image, scan_barcode, delete_temp_image

@login_required
def upload_barcode(request):
    """Handles barcode image upload & redirects after scanning."""
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        image_path = save_temp_image(form.cleaned_data['image'])
        barcode = scan_barcode(image_path)
        delete_temp_image(image_path)

        if barcode:
            barcode = barcode.decode("utf-8") if isinstance(barcode, bytes) else str(barcode)  # Ensure string format
            return redirect('add_purchase', barcode=barcode)

        form.add_error('image', "No barcode detected. Try again.")

    return render(request, 'purchases/upload_barcode.html', {'form': form})

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
