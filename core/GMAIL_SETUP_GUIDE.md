# Gmail SMTP Ayarları - Detaylı Rehber

## 🚨 SMTPAuthenticationError Çözümü

Bu hata Gmail'in güvenlik ayarları nedeniyle oluşur. Aşağıdaki adımları takip edin:

### 1. Gmail'de 2 Adımlı Doğrulama Açın

1. Gmail hesabınıza giriş yapın
2. Google Hesabınıza gidin: https://myaccount.google.com/
3. "Güvenlik" sekmesine tıklayın
4. "2 Adımlı Doğrulama"yı bulun ve "Açık" yapın
5. Telefon numaranızı doğrulayın

### 2. Uygulama Şifresi Oluşturun

1. Google Hesabınızda "Güvenlik" sekmesinde kalın
2. "2 Adımlı Doğrulama" bölümünde "Uygulama Şifreleri"ne tıklayın
3. "Uygulama Seç" dropdown'undan "Diğer (Özel ad)" seçin
4. İsim olarak "Django E-Ticaret" yazın
5. "Oluştur" butonuna tıklayın
6. **16 haneli şifreyi kopyalayın** (örn: abcd efgh ijkl mnop)

### 3. Django Ayarlarını Güncelleyin

`core/core/settings.py` dosyasında şu ayarları güncelleyin:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Gmail adresinizi yazın
EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'  # Uygulama şifrenizi yazın (boşluklar olmadan)
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### 4. Test Edin

```bash
python test_email.py
```

## 🔍 Sorun Giderme

### Hala Hata Alıyorsanız:

1. **2 Adımlı Doğrulama Açık mı?**
   - Google Hesabınızda kontrol edin
   - Açık değilse önce bunu açın

2. **Uygulama Şifresi Doğru mu?**
   - 16 haneli şifreyi tam olarak kopyaladınız mı?
   - Boşlukları kaldırdınız mı?

3. **Gmail Adresi Doğru mu?**
   - Gmail adresinizi tam olarak yazdınız mı?

4. **Gmail Güvenlik Ayarları**
   - Gmail'de "Daha az güvenli uygulama erişimi" açık olmalı
   - Veya uygulama şifresi kullanmalısınız (önerilen)

## 📧 Alternatif Test

Eğer hala sorun yaşıyorsanız, geçici olarak şu ayarları deneyin:

```python
# Test için geçici ayarlar
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Bu ayar email'leri konsola yazdırır, böylece sistem çalışıp çalışmadığını test edebilirsiniz.

## 🔒 Güvenlik Notları

- Uygulama şifrenizi kimseyle paylaşmayın
- Production'da environment variables kullanın
- Şifrenizi version control'e commit etmeyin

## 📞 Yardım

Eğer hala sorun yaşıyorsanız:
1. Gmail hesabınızın güvenlik ayarlarını kontrol edin
2. Yeni bir uygulama şifresi oluşturun
3. Farklı bir Gmail hesabı deneyin 