import os
from django.conf import settings
from pyzxing import BarCodeReader
from .models import Purchase

def save_temp_image(image):
    """Saves uploaded image temporarily for processing."""
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp_" + image.name)
    with open(temp_path, "wb+") as destination:
        for chunk in image.chunks():
            destination.write(chunk)
    return temp_path

def scan_barcode(image_path):
    """Scans barcode from an image and returns its data."""
    reader = BarCodeReader()
    results = reader.decode(image_path)
    return results[0]['raw'] if results else None

def delete_temp_image(image_path):
    """Deletes the temporary image after processing."""
    if os.path.exists(image_path):
        os.remove(image_path)
