# Email Doğrulama Sistemi Kurulum Rehberi

Bu projeye email doğrulama sistemi başarıyla eklenmiştir. Aşağıdaki adımları takip ederek sistemi aktif hale getirebilirsiniz.

## 1. Gmail Ayarları

### Gmail Uygulama Şifresi Oluşturma
1. Gmail hesabınıza giriş yapın
2. Google Hesabınıza gidin: https://myaccount.google.com/
3. "Güvenlik" sekmesine tıklayın
4. "2 Adımlı Doğrulama"yı etkinleştirin
5. "Uygulama Şifreleri"ne tıklayın
6. "Diğer" seçeneğini seçin ve bir isim verin (örn: "Django E-Ticaret")
7. Oluşturulan 16 haneli şifreyi kopyalayın

## 2. Django Ayarları

`core/core/settings.py` dosyasında aşağıdaki ayarları güncelleyin:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Gmail adresinizi buraya yazın
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail uygulama şifrenizi buraya yazın
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## 3. Gerekli Paketleri Yükleme

```bash
pip install django-allauth==0.60.1
```

## 4. Veritabanı Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Sistem Özellikleri

### Yeni Kayıt Sistemi
- Kullanıcı kayıt olduğunda hesabı otomatik olarak deaktif olur
- Email doğrulama linki otomatik olarak gönderilir
- Doğrulama linki 7 gün geçerlidir

### Giriş Sistemi
- Email doğrulanmamış hesaplar giriş yapamaz
- Login sayfasında "Email Doğrulama Linkini Tekrar Gönder" linki bulunur

### Email Doğrulama
- Kullanıcı email linkine tıkladığında hesabı aktif olur
- Süresi dolmuş linkler için yeni doğrulama emaili istenebilir

## 6. Test Etme

1. Yeni bir kullanıcı kaydı oluşturun
2. Email kutunuzu kontrol edin
3. Doğrulama linkine tıklayın
4. Giriş yapmayı deneyin

## 7. Güvenlik Notları

- Gmail uygulama şifrenizi güvenli tutun
- Production ortamında environment variables kullanın
- Email ayarlarını version control'e commit etmeyin

## 8. Sorun Giderme

### Email Gönderilmiyor
- Gmail ayarlarını kontrol edin
- Uygulama şifresinin doğru olduğundan emin olun
- 2 Adımlı Doğrulama'nın açık olduğunu kontrol edin

### Doğrulama Linki Çalışmıyor
- Token'ın süresi dolmuş olabilir
- Veritabanında EmailVerification kaydının olduğunu kontrol edin

## 9. Production Ayarları

Production ortamında aşağıdaki değişiklikleri yapın:

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# Email ayarlarını environment variables'dan alın
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Doğrulama URL'ini güncelleyin
verification_url = f"https://yourdomain.com/verify-email/{verification.token}/"
``` 