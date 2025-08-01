#!/usr/bin/env python
"""
Email Doğrulama Sistemi Test Scripti
Bu script email doğrulama sisteminin çalışıp çalışmadığını test eder.
"""

import os
import sys
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from AppTicaret.models import EmailVerification
from AppTicaret.views import send_verification_email

def test_email_verification():
    """Email doğrulama sistemini test eder"""
    print("Email Doğrulama Sistemi Test Ediliyor...")
    print("=" * 50)
    
    # Test kullanıcısı oluştur
    test_email = "test@example.com"
    
    # Eğer test kullanıcısı varsa sil
    User.objects.filter(email=test_email).delete()
    
    # Yeni test kullanıcısı oluştur
    user = User.objects.create_user(
        username=test_email,
        email=test_email,
        first_name="Test",
        last_name="User",
        password="testpass123"
    )
    user.is_active = False
    user.save()
    
    print(f"Test kullanıcısı oluşturuldu: {user.email}")
    
    # Email doğrulama kaydı oluştur
    verification = EmailVerification.objects.create(user=user)
    print(f"Email doğrulama kaydı oluşturuldu: {verification.token}")
    
    # Email göndermeyi dene
    try:
        send_verification_email(user, verification)
        print("✅ Email başarıyla gönderildi!")
        print(f"📧 Doğrulama URL: http://localhost:8000/verify-email/{verification.token}/")
    except Exception as e:
        print(f"❌ Email gönderilirken hata oluştu: {e}")
        print("💡 Gmail ayarlarını kontrol edin!")
    
    # Token süresi kontrolü
    print(f"⏰ Token oluşturulma zamanı: {verification.created_at}")
    print(f"⏰ Token geçerlilik süresi: 7 gün")
    print(f"⏰ Token süresi dolmuş mu: {verification.is_expired()}")
    
    print("\n" + "=" * 50)
    print("Test tamamlandı!")
    
    # Temizlik
    user.delete()
    print("Test kullanıcısı silindi.")

if __name__ == "__main__":
    test_email_verification() 