import os
import pyzxing
from django.conf import settings


def save_temp_image(image):
    """
    Saves uploaded image temporarily for processing.
    """
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp_" + image.name)
    with open(temp_path, "wb+") as destination:
        for chunk in image.chunks():
            destination.write(chunk)
    return temp_path


def scan_barcode(image_path):
    """
    Scans barcode from an image, handles missing barcodes gracefully.
    """
    try:
        reader = pyzxing.BarCodeReader()
        result = reader.decode(image_path)

        if not result or not isinstance(result, list) or len(result) == 0:
            print("No barcode detected.")
            return None

        if 'raw' in result[0]:
            return result[0]['raw']
        else:
            return None

    except Exception as e:
        return None


def delete_temp_image(image_path):
    """
    Deletes the temporary image after processing.
    """
    if os.path.exists(image_path):
        os.remove(image_path)
