import os
import django
import requests
from django.core.files.base import ContentFile
from io import BytesIO
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from AppTicaret.models import Product, ProductImage

# Örnek saat görseli URL'leri
WATCH_IMAGE_URLS = [
    'https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b',
    'https://images.unsplash.com/photo-1465101046530-73398c7f28ca',
    'https://images.unsplash.com/photo-1506744038136-46273834b3fb',
    'https://images.unsplash.com/photo-1519125323398-675f0ddb6308',
    'https://images.unsplash.com/photo-1512436991641-6745cdb1723f',
    'https://images.unsplash.com/photo-1465101178521-c1a9136a3b99',
    'https://images.unsplash.com/photo-1517841905240-472988babdf9',
    'https://images.unsplash.com/photo-1519125323398-675f0ddb6308',
    'https://images.unsplash.com/photo-1465101046530-73398c7f28ca',
    'https://images.unsplash.com/photo-1512436991641-6745cdb1723f',
]

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None

def add_missing_images():
    products = Product.objects.all()
    added = 0
    for product in products:
        if product.images.count() == 0:
            img_url = random.choice(WATCH_IMAGE_URLS)
            img_content = download_image(img_url)
            if img_content:
                ext = 'jpg'
                filename = f"{product.model.replace(' ', '_')}_auto.{ext}"
                product_image = ProductImage(
                    product=product,
                    alt_text=f"{product.brand.brand} {product.model}",
                    is_primary=True,
                    order=0
                )
                product_image.image.save(filename, ContentFile(img_content), save=True)
                print(f"{product.model} için görsel eklendi.")
                added += 1
            else:
                print(f"{product.model} için görsel indirilemedi!")
        else:
            print(f"{product.model} zaten görsele sahip, atlanıyor.")
    print(f"Toplam eklenen görsel: {added}")

if __name__ == "__main__":
    add_missing_images() 