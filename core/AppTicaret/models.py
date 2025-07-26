from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    brand = models.CharField(max_length=250)
    image = models.ImageField(upload_to='Brand Image')

    def __str__(self):
        return self.brand
    
    class Meta:
        verbose_name_plural = "Markalar"


class Gender(models.Model):
    gender = models.CharField(max_length=250)

    def __str__(self):
        return self.gender
    
    class Meta:
        verbose_name_plural = "Cinsiyetler"


class Color(models.Model):
    color = models.CharField(max_length=250)

    def __str__(self):
        return self.color
    
    class Meta:
        verbose_name_plural = "Renkler"


class CaseShape(models.Model):
    case_shape = models.CharField(max_length=250)

    def __str__(self):
        return self.case_shape
    
    class Meta:
        verbose_name_plural = "Kasa Şekilleri"


class StrapType(models.Model):
    strap_type = models.CharField(max_length=250)

    def __str__(self):
        return self.strap_type
    
    class Meta:
        verbose_name_plural = "Kayış Türleri"


class GlassFeature(models.Model):
    glass_feature = models.CharField(max_length=250)

    def __str__(self):
        return self.glass_feature
    
    class Meta:
        verbose_name_plural = "Cam Özellikleri"


class Style(models.Model):
    style = models.CharField(max_length=250)

    def __str__(self):
        return self.style
    
    class Meta:
        verbose_name_plural = "Stiller"


class Mechanism(models.Model):
    mechanism = models.CharField(max_length=250)

    def __str__(self):
        return self.mechanism
    
    class Meta:
        verbose_name_plural = "Mekanizmalar"


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='Product Images', verbose_name="Ürün Görseli")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Alt Metin")
    is_primary = models.BooleanField(default=False, verbose_name="Ana Görsel")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.model} - {self.alt_text or 'Görsel'}"

    def save(self, *args, **kwargs):
        # Eğer bu görsel ana görsel olarak işaretlendiyse, diğer görselleri ana görsel olmaktan çıkar
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Ürün Görselleri"
        ordering = ['order', 'created_at']


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    model = models.CharField(max_length=250)
    description = models.TextField()
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0, verbose_name="Stok Miktarı")
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    case_shape = models.ForeignKey(CaseShape, on_delete=models.CASCADE)
    strap_type = models.ForeignKey(StrapType, on_delete=models.CASCADE)
    glass_feature = models.ForeignKey(GlassFeature, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    mechanism = models.ForeignKey(Mechanism, on_delete=models.CASCADE)

    def __str__(self):
        return self.model
    
    @property
    def is_in_stock(self):
        """Ürünün stokta olup olmadığını kontrol eder"""
        return self.stock > 0
    
    @property
    def stock_status(self):
        """Stok durumunu metin olarak döndürür"""
        if self.stock == 0:
            return "Stokta Yok"
        elif self.stock <= 5:
            return f"Son {self.stock} Adet"
        else:
            return "Stokta Var"
    
    @property
    def primary_image(self):
        """Ana görseli döndürür"""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image
        # Ana görsel yoksa ilk görseli döndür
        first_image = self.images.first()
        return first_image.image if first_image else None
    
    @property
    def all_images(self):
        """Tüm görselleri sıralı şekilde döndürür"""
        return self.images.all().order_by('order', 'created_at')
    
    class Meta:
        verbose_name_plural = "Ürünler"



class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.model
    
    class Meta:
        verbose_name_plural = "Sepetler"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Profiller"
    
class Address(models.Model):
    ADDRESS_TYPES = [
        ('home', 'Ev'),
        ('work', 'İş'),
        ('other', 'Diğer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Adres Başlığı")  # Ev, İş, vs.
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    city = models.CharField(max_length=50, verbose_name="İl")
    district = models.CharField(max_length=50, verbose_name="İlçe")
    neighborhood = models.CharField(max_length=50, verbose_name="Mahalle")
    address = models.TextField(verbose_name="Açık Adres")
    is_default = models.BooleanField(default=False, verbose_name="Varsayılan Adres")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.first_name} {self.last_name}"

    def get_full_address(self):
        return f"{self.address}, {self.neighborhood}, {self.district}, {self.city}"

    def save(self, *args, **kwargs):
        # Eğer bu adres varsayılan olarak işaretlendiyse, diğer adresleri varsayılan olmaktan çıkar
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Adresler"
        ordering = ['-is_default', '-created_at']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Favoriler"

class Comment(models.Model):
    RATING_CHOICES = [
        (1, '1 Yıldız'),
        (2, '2 Yıldız'),
        (3, '3 Yıldız'),
        (4, '4 Yıldız'),
        (5, '5 Yıldız'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ürün")
    comment = models.TextField(max_length=500, verbose_name="Yorum")
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name="Puan")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Yorum Tarihi")
    is_verified_purchase = models.BooleanField(default=False, verbose_name="Doğrulanmış Satın Alma")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.product.model} - {self.rating} Yıldız"
    
    class Meta:
        verbose_name_plural = "Yorumlar"
        ordering = ['-create_date']

import random
import string

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('processing', 'İşleniyor'),
        ('shipped', 'Kargoda'),
        ('delivered', 'Teslim Edildi'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Teslimat Adresi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Kargo Takip Numarası")
    
    def __str__(self):
        return f"Sipariş #{self.id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Eğer takip numarası yoksa otomatik oluştur
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)
    
    def generate_tracking_number(self):
        """Kargo takip numarası oluştur"""
        # TR + 10 haneli rastgele sayı
        numbers = ''.join(random.choices(string.digits, k=10))
        return f"TR{numbers}"
    
    class Meta:
        verbose_name_plural = "Siparişler"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()  # Sipariş anındaki fiyat
    
    @property
    def total_price(self):
        """Sipariş öğesinin toplam fiyatını hesaplar"""
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.product.model} x {self.quantity}"
    
    class Meta:
        verbose_name_plural = "Sipariş Ürünleri"

