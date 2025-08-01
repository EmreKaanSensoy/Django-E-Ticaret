# Alternatif Email Sağlayıcıları

Gmail ile sorun yaşıyorsanız, aşağıdaki alternatifleri deneyebilirsiniz:

## 1. Outlook/Hotmail (En Kolay)

### Ayarlar:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'  # Normal şifre
DEFAULT_FROM_EMAIL = 'your-email@outlook.com'
```

### Avantajları:
- ✅ Uygulama şifresi gerektirmez
- ✅ Normal şifre ile çalışır
- ✅ Kurulum kolay

## 2. Yahoo Mail

### Ayarlar:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@yahoo.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Uygulama şifresi gerekli
DEFAULT_FROM_EMAIL = 'your-email@yahoo.com'
```

## 3. Yandex Mail

### Ayarlar:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@yandex.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@yandex.com'
```

## 4. Test İçin Console Backend

Eğer hiçbiri çalışmazsa, test için:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Bu ayar email'leri terminal'de gösterir.

## 5. Ücretsiz Email Servisleri

### SendGrid (Ücretsiz 100 email/gün)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
DEFAULT_FROM_EMAIL = 'your-email@yourdomain.com'
```

### Mailgun (Ücretsiz 5000 email/ay)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@yourdomain.mailgun.org'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
DEFAULT_FROM_EMAIL = 'your-email@yourdomain.com'
```

## 🚀 Önerilen Çözüm

1. **Outlook/Hotmail** kullanın (en kolay)
2. Normal şifrenizi kullanın
3. Hiçbir ek ayar gerektirmez

## 📝 Test Etme

Ayarları değiştirdikten sonra:

```bash
python test_email.py
```

## 🔧 Sorun Giderme

### Outlook/Hotmail için:
- Normal şifrenizi kullanın
- 2 Adımlı Doğrulama açık olabilir
- Güvenlik ayarlarını kontrol edin

### Genel Sorunlar:
- Port 587 kullanın
- TLS açık olmalı
- Şifrede özel karakterler varsa dikkatli olun 