# Gmail Uygulama Şifresi - Adım Adım Rehber

## 🚀 Adım 1: Gmail'de 2 Adımlı Doğrulama Açın

1. **Gmail hesabınıza giriş yapın**
2. **Google Hesabınıza gidin:** https://myaccount.google.com/
3. **"Güvenlik" sekmesine tıklayın**
4. **"2 Adımlı Doğrulama"yı bulun**
5. **"Açık" yapın**
6. **Telefon numaranızı doğrulayın**

## 🔑 Adım 2: Uygulama Şifresi Oluşturun

1. **Google Hesabınızda "Güvenlik" sekmesinde kalın**
2. **"2 Adımlı Doğrulama" bölümünde "Uygulama Şifreleri"ne tıklayın**
3. **"Uygulama Seç" dropdown'undan "Diğer (Özel ad)" seçin**
4. **İsim olarak "Django E-Ticaret" yazın**
5. **"Oluştur" butonuna tıklayın**
6. **16 haneli şifreyi kopyalayın** (örn: `abcd efgh ijkl mnop`)

## ⚙️ Adım 3: Django Ayarlarını Güncelleyin

`core/core/settings.py` dosyasında şu satırları bulun ve değiştirin:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'  # Buraya Gmail adresinizi yazın
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # Buraya uygulama şifrenizi yazın (boşlukları kaldırın)
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Buraya da aynı Gmail adresini yazın
```

**Örnek:**
```python
EMAIL_HOST_USER = 'emrekaan@gmail.com'
EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'  # Boşlukları kaldırın: abcdefghijklmnop
DEFAULT_FROM_EMAIL = 'emrekaan@gmail.com'
```

## 🧪 Adım 4: Test Edin

Ayarları yaptıktan sonra:

```bash
python test_email.py
```

## ❌ Sorun Giderme

### Hata: "Username and Password not accepted"

**Çözüm:**
1. **2 Adımlı Doğrulama açık mı?** Kontrol edin
2. **Uygulama şifresini doğru kopyaladınız mı?** Boşlukları kaldırın
3. **Gmail adresini doğru yazdınız mı?** Tam adresi yazın

### Hata: "Authentication unsuccessful"

**Çözüm:**
1. **Yeni bir uygulama şifresi oluşturun**
2. **Şifrede özel karakterler varsa dikkatli olun**
3. **Gmail hesabınızın güvenlik ayarlarını kontrol edin**

## 📞 Yardım

Eğer hala sorun yaşıyorsanız:
1. Gmail hesabınızın güvenlik ayarlarını kontrol edin
2. Yeni bir uygulama şifresi oluşturun
3. Farklı bir Gmail hesabı deneyin

## 🔒 Güvenlik Notları

- Uygulama şifrenizi kimseyle paylaşmayın
- Production'da environment variables kullanın
- Şifrenizi version control'e commit etmeyin 