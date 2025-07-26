import os
import django
from django.conf import settings

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from AppTicaret.models import Product, ProductImage

def migrate_product_images():
    """Mevcut ürün görsellerini yeni ProductImage modeline taşır"""
    products = Product.objects.all()
    
    for product in products:
        # Eğer ürünün zaten ProductImage'leri varsa atla
        if product.images.exists():
            print(f"Ürün {product.model} zaten görselleri var, atlanıyor...")
            continue
            
        # Eğer ürünün eski image alanı varsa ve boş değilse
        if hasattr(product, 'image') and product.image:
            try:
                # Yeni ProductImage oluştur
                ProductImage.objects.create(
                    product=product,
                    image=product.image,
                    alt_text=f"{product.brand.brand} {product.model}",
                    is_primary=True,
                    order=0
                )
                print(f"Ürün {product.model} için görsel taşındı")
            except Exception as e:
                print(f"Ürün {product.model} için görsel taşınırken hata: {e}")
        else:
            print(f"Ürün {product.model} için görsel bulunamadı")

if __name__ == "__main__":
    print("Ürün görselleri taşınıyor...")
    migrate_product_images()
    print("Taşıma tamamlandı!") 