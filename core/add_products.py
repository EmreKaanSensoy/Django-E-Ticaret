import os
import sys
import django
import requests
from PIL import Image
from io import BytesIO
import tempfile

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from AppTicaret.models import Product, Brand, Gender, Color, CaseShape, StrapType, GlassFeature, Style, Mechanism

def download_image(url, filename):
    """İnternetten görsel indir"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Görseli PIL ile aç ve kontrol et
        img = Image.open(BytesIO(response.content))
        
        # Geçici dosya oluştur
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        img.save(temp_file.name, 'JPEG')
        
        return temp_file.name
    except Exception as e:
        print(f"Görsel indirme hatası: {e}")
        return None

def create_or_get_model(model_class, name_field, name_value):
    """Model oluştur veya mevcut olanı getir"""
    try:
        obj, created = model_class.objects.get_or_create(**{name_field: name_value})
        if created:
            print(f"Yeni {model_class.__name__} oluşturuldu: {name_value}")
        return obj
    except Exception as e:
        print(f"{model_class.__name__} oluşturma hatası: {e}")
        return None

def add_products():
    """Ürünleri veritabanına ekle"""
    
    # Örnek ürün verileri
    products_data = [
        {
            'brand': 'Rolex',
            'model': 'Submariner',
            'description': 'Klasik dalış saati, su geçirmez ve dayanıklı',
            'price': 85000,
            'gender': 'Erkek',
            'color': 'Siyah',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Metal',
            'glass_feature': 'Sapphire',
            'style': 'Spor',
            'mechanism': 'Otomatik',
            'image_url': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Omega',
            'model': 'Speedmaster',
            'description': 'Ay yürüyüşünde kullanılan efsanevi kronograf',
            'price': 65000,
            'gender': 'Erkek',
            'color': 'Siyah',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Metal',
            'glass_feature': 'Sapphire',
            'style': 'Spor',
            'mechanism': 'Manuel',
            'image_url': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Cartier',
            'model': 'Tank',
            'description': 'Zarif ve klasik tasarım, lüks saat koleksiyonu',
            'price': 45000,
            'gender': 'Kadın',
            'color': 'Altın',
            'case_shape': 'Dikdörtgen',
            'strap_type': 'Deri',
            'glass_feature': 'Mineral',
            'style': 'Klasik',
            'mechanism': 'Quartz',
            'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Seiko',
            'model': 'Presage',
            'description': 'Japon kalitesi, otomatik mekanizma',
            'price': 8500,
            'gender': 'Erkek',
            'color': 'Mavi',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Deri',
            'glass_feature': 'Hardlex',
            'style': 'Klasik',
            'mechanism': 'Otomatik',
            'image_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Tissot',
            'model': 'T-Touch',
            'description': 'Dokunmatik ekranlı akıllı saat',
            'price': 12000,
            'gender': 'Erkek',
            'color': 'Gri',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Kauçuk',
            'glass_feature': 'Sapphire',
            'style': 'Spor',
            'mechanism': 'Quartz',
            'image_url': 'https://images.unsplash.com/photo-1544117519-31a4b719223d?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Swatch',
            'model': 'Classic',
            'description': 'Renkli ve eğlenceli tasarım',
            'price': 2500,
            'gender': 'Unisex',
            'color': 'Beyaz',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Plastik',
            'glass_feature': 'Mineral',
            'style': 'Casual',
            'mechanism': 'Quartz',
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Casio',
            'model': 'G-Shock',
            'description': 'Dayanıklı ve su geçirmez spor saati',
            'price': 1800,
            'gender': 'Erkek',
            'color': 'Siyah',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Kauçuk',
            'glass_feature': 'Mineral',
            'style': 'Spor',
            'mechanism': 'Quartz',
            'image_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Fossil',
            'model': 'Grant',
            'description': 'Amerikan tarzı klasik saat',
            'price': 3500,
            'gender': 'Erkek',
            'color': 'Kahverengi',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Deri',
            'glass_feature': 'Mineral',
            'style': 'Klasik',
            'mechanism': 'Quartz',
            'image_url': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Michael Kors',
            'model': 'Bradshaw',
            'description': 'Şık ve modern kadın saati',
            'price': 4200,
            'gender': 'Kadın',
            'color': 'Gümüş',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Metal',
            'glass_feature': 'Mineral',
            'style': 'Modern',
            'mechanism': 'Quartz',
            'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500&h=500&fit=crop'
        },
        {
            'brand': 'Citizen',
            'model': 'Eco-Drive',
            'description': 'Güneş enerjili çevre dostu saat',
            'price': 6800,
            'gender': 'Erkek',
            'color': 'Mavi',
            'case_shape': 'Yuvarlak',
            'strap_type': 'Metal',
            'glass_feature': 'Mineral',
            'style': 'Klasik',
            'mechanism': 'Quartz',
            'image_url': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=500&h=500&fit=crop'
        }
    ]
    
    print("Ürün ekleme işlemi başlıyor...")
    
    for i, product_data in enumerate(products_data, 1):
        try:
            print(f"\n{i}. Ürün ekleniyor: {product_data['brand']} {product_data['model']}")
            
            # Model nesnelerini oluştur veya getir
            brand = create_or_get_model(Brand, 'brand', product_data['brand'])
            gender = create_or_get_model(Gender, 'gender', product_data['gender'])
            color = create_or_get_model(Color, 'color', product_data['color'])
            case_shape = create_or_get_model(CaseShape, 'case_shape', product_data['case_shape'])
            strap_type = create_or_get_model(StrapType, 'strap_type', product_data['strap_type'])
            glass_feature = create_or_get_model(GlassFeature, 'glass_feature', product_data['glass_feature'])
            style = create_or_get_model(Style, 'style', product_data['style'])
            mechanism = create_or_get_model(Mechanism, 'mechanism', product_data['mechanism'])
            
            if not all([brand, gender, color, case_shape, strap_type, glass_feature, style, mechanism]):
                print(f"Model oluşturma hatası, ürün atlanıyor: {product_data['brand']} {product_data['model']}")
                continue
            
            # Görseli indir
            image_path = download_image(product_data['image_url'], f"{product_data['brand']}_{product_data['model']}.jpg")
            
            if not image_path:
                print(f"Görsel indirme hatası, ürün atlanıyor: {product_data['brand']} {product_data['model']}")
                continue
            
            # Ürünü oluştur
            product = Product.objects.create(
                brand=brand,
                model=product_data['model'],
                description=product_data['description'],
                price=product_data['price'],
                gender=gender,
                color=color,
                case_shape=case_shape,
                strap_type=strap_type,
                glass_feature=glass_feature,
                style=style,
                mechanism=mechanism
            )
            
            # Görseli ürüne ekle
            with open(image_path, 'rb') as img_file:
                from django.core.files import File
                product.image.save(f"{product_data['brand']}_{product_data['model']}.jpg", File(img_file), save=True)
            
            # Geçici dosyayı sil
            os.unlink(image_path)
            
            print(f"✅ Başarıyla eklendi: {product_data['brand']} {product_data['model']} - {product_data['price']} ₺")
            
        except Exception as e:
            print(f"❌ Hata: {product_data['brand']} {product_data['model']} - {e}")
            continue
    
    print(f"\n🎉 Toplam {len(products_data)} ürün işlendi!")
    print("Ürün ekleme işlemi tamamlandı.")

if __name__ == '__main__':
    add_products() 