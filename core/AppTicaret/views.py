from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, CartProduct, Profile, Address, Favorite, Comment, Order, OrderItem, Brand, Gender, Color, CaseShape, StrapType, GlassFeature, Style, Mechanism

from django.db.models import Q, Sum, Avg
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def ProductQuantity(request):
    if request.user.is_authenticated:
        return CartProduct.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    return 0

def index(request):
    products = Product.objects.all()
    favorite_product_ids = []
    if request.user.is_authenticated:
        favorite_product_ids = list(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    context = {
        'products': products,
        'product_quantity': ProductQuantity(request),
        'favorite_product_ids': favorite_product_ids,
    }
    return render(request, 'index.html', context)

def Category(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    genders = Gender.objects.all()
    colors = Color.objects.all()
    case_shapes = CaseShape.objects.all()
    strap_types = StrapType.objects.all()
    glass_features = GlassFeature.objects.all()
    styles = Style.objects.all()
    mechanisms = Mechanism.objects.all()

    # Filtreleme işlemleri
    filters = Q()
    if "brand" in request.GET:
        brand_names = request.GET.getlist("brand")
        for brand_name in brand_names:
            filters |= Q(brand__brand=brand_name)

    if "color" in request.GET:
        color_names = request.GET.getlist("color")
        for color_name in color_names:
            filters |= Q(color__color=color_name)

    if "case_shape" in request.GET:
        case_shape_names = request.GET.getlist("case_shape")
        for case_shape_name in case_shape_names:
            filters |= Q(case_shape__case_shape=case_shape_name)

    if "strap_type" in request.GET:
        strap_type_names = request.GET.getlist("strap_type")
        for strap_type_name in strap_type_names:
            filters |= Q(strap_type__strap_type=strap_type_name)

    if "glass_feature" in request.GET:
        glass_feature_names = request.GET.getlist("glass_feature")
        for glass_feature_name in glass_feature_names:
            filters |= Q(glass_feature__glass_feature=glass_feature_name)

    if "style" in request.GET:
        style_names = request.GET.getlist("style")
        for style_name in style_names:
            filters |= Q(style__style=style_name)

    if "mechanism" in request.GET:
        mechanism_names = request.GET.getlist("mechanism")
        for mechanism_name in mechanism_names:
            filters |= Q(mechanism__mechanism=mechanism_name)
            
    if "min_price" in request.GET and "max_price" in request.GET and request.GET.get("max_price") != "":
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        if min_price == "":
            min_price = 0

        filters &= Q(price__gte=min_price) & Q(price__lte=max_price)

    if "gender" in request.GET:
        filters &= Q(gender=request.GET.get("gender"))

    products = products.filter(filters)

    paginator = Paginator(products, 1)  # Her sayfada 1 ürün
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    favorite_product_ids = []
    if request.user.is_authenticated:
        favorite_product_ids = list(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'products': products,
        'brands': brands,
        'gender': genders,
        'colors': colors,
        'case_shapes': case_shapes,
        'strap_types': strap_types,
        'glass_features': glass_features,
        'styles': styles,
        'mechanisms': mechanisms,
        'product_quantity': ProductQuantity(request),
        'favorite_product_ids': favorite_product_ids,
    }
    return render(request, 'category.html', context)

@login_required(login_url='login')
def Cart(request):  
    cart_products = CartProduct.objects.filter(user=request.user)
    cargo= 29.99 
    total_price = 0
    product_total_price = 0

    for product in cart_products:
        product_total_price += product.product.price * product.quantity
    total_price = product_total_price + cargo

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if "update_quantity" in request.POST:
            quantity = int(request.POST.get("quantity", 1))
            cart_product = CartProduct.objects.get(id=product_id)
            
            # Stok kontrolü
            if quantity > cart_product.product.stock:
                messages.error(request, f"Yeterli stok bulunmamaktadır! Mevcut stok: {cart_product.product.stock}")
                return redirect('cart')
            
            cart_product.quantity = max(1, quantity)
            cart_product.save()
        else:
            cart_product = CartProduct.objects.get(id=product_id)
            cart_product.delete()
        return redirect('cart')

    context = {
        'cart_products': cart_products,
        'product_total_price': product_total_price,
        'total_price': total_price,
        'cargo': cargo,
        'product_quantity': ProductQuantity(request),
    }

    return render(request, 'cart.html', context)

@login_required(login_url='login')
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    adress, created = Address.objects.get_or_create(user=user)

    if request.method == "POST":
        if "change_password" in request.POST:
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            if new_password == confirm_password:
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    return redirect('login')
                else:
                    messages.error(request, "Mevcut Şifreniz Hatalı")
            else:
                messages.error(request, "Yeni Şifreler Eşleşmiyor")
            
        if "update_profile" in request.POST:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            birthday = request.POST.get("birthday")

            if user.email != email:
                if not User.objects.filter(email=email).exists():
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    profile.phone = phone
                    profile.birthday = birthday
                    user.save()
                    profile.save()
                    messages.success(request, "Profil bilgileriniz güncellendi.")
                    return redirect('profile')
                else:
                    messages.error(request, "Bu E-Posta Adresi Başka Bir Kullanıcı Tarafından Kullanılıyor.")
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                profile.phone = phone
                profile.birthday = birthday
                user.save()
                profile.save()
                messages.success(request, "Profil bilgileriniz güncellendi.")
                return redirect('profile')
        
        if "update_address" in request.POST:
            city = request.POST.get("city")
            district = request.POST.get("district")
            neighborhood = request.POST.get("neighborhood")
            address = request.POST.get("address")
            
            adress.city = city
            adress.district = district
            adress.neighborhood = neighborhood
            adress.address = address
            adress.save()
            
            messages.success(request, "Adres bilgileriniz güncellendi.")
            return redirect('profile')
            
    context = {
        'profile': profile,
        'adress': adress,
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'user/profile.html', context)

def ProductDetail(request, product_id):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product).order_by('-create_date')

    # Favori kontrolü
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    # Kullanıcının yorum yapabilir mi kontrolü
    can_comment = False
    if request.user.is_authenticated:
        # Kullanıcının bu ürünü satın alıp almadığını kontrol et
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered'
        ).exists()
        
        # Kullanıcının bu ürün için daha önce yorum yapıp yapmadığını kontrol et
        has_commented = Comment.objects.filter(user=request.user, product=product).exists()
        
        can_comment = has_purchased and not has_commented
    
    # Ortalama puan hesapla
    if comments.exists():
        average_rating = comments.aggregate(avg_rating=Avg('rating'))['avg_rating']
    else:
        average_rating = 0

    context = {
        'product': product,
        'product_quantity': ProductQuantity(request),
        'comments': comments,
        'is_favorite': is_favorite,
        'can_comment': can_comment,
        'average_rating': average_rating,
    }
    return render(request, 'product_detail.html', context)

def Login(request):
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user is not None:
                    login(request, user)
                    return redirect('index')
            else:
                messages.error(request, "Şifreniz Hatalı")    
        else:
            messages.error(request, "Bu E-Posta Adresi Kayıtlı Değil")
    return render(request, 'user/login.html')

def Register(request):
    if request.method == "POST":
        first_name = request.POST.get("name")
        last_name = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not first_name or not last_name or not email or not password:
            messages.error(request, "Lütfen tüm alanları doldurun.")
            return render(request, 'user/register.html')

        if not User.objects.filter(email=email).exists():
            try:
                user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password=password)
                user.is_active = True
                user.save()
                
                profile = Profile.objects.create(user=user)
                
                # Kullanıcıyı otomatik giriş yap
                login(request, user)
                messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
                return redirect('index')
            except Exception as e:
                messages.error(request, f"Kayıt sırasında bir hata oluştu: {e}")
        else:
            messages.error(request, "Bu E-Posta Adresi Zaten Kayıtlı")

    return render(request, 'user/register.html')

def Logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "index"))






def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response

def Favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    favorite_product_ids = list(favorites.values_list('product_id', flat=True))
    context = {
        'favorites': favorites,
        'product_quantity': ProductQuantity(request),
        'favorite_product_ids': favorite_product_ids,
    }
    return render(request, 'favorite.html', context)

def remove_favorite(request, product_id):
    if request.user.is_authenticated:
        Favorite.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('favorite')

def toggle_favorite(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = Product.objects.get(id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        quantity = int(request.POST.get("quantity", 1))
        
        # Stok kontrolü
        if not product.is_in_stock:
            messages.error(request, f"{product.model} şu anda stokta bulunmamaktadır!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        if quantity > product.stock:
            messages.error(request, f"Yeterli stok bulunmamaktadır! Mevcut stok: {product.stock}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        # Sepette bu ürün var mı kontrol et
        cart_product, created = CartProduct.objects.get_or_create(
            user=request.user, 
            product=product
        )
        
        if not created:
            # Ürün zaten sepette varsa miktarı artır
            new_quantity = cart_product.quantity + quantity
            if new_quantity > product.stock:
                messages.error(request, f"Yeterli stok bulunmamaktadır! Mevcut stok: {product.stock}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            cart_product.quantity = new_quantity
        else:
            # Yeni ürün ekleniyorsa miktarı ayarla
            cart_product.quantity = quantity
            
        cart_product.save()
        messages.success(request, f"{product.model} sepete eklendi!")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
def checkout(request):
    if request.method == "POST":
        address_id = request.POST.get('shipping_address')
        if not address_id:
            messages.error(request, "Lütfen teslimat adresi seçin!")
            return redirect('checkout')
        
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, "Seçilen adres bulunamadı!")
            return redirect('checkout')
        
        cart_products = CartProduct.objects.filter(user=request.user)
        if not cart_products.exists():
            messages.error(request, "Sepetinizde ürün bulunmamaktadır!")
            return redirect('cart')
        
        total_amount = sum(product.product.price * product.quantity for product in cart_products)
        total_amount += 29.99  # Kargo ücreti
        
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=address
        )
        
        for cart_product in cart_products:
            OrderItem.objects.create(
                order=order,
                product=cart_product.product,
                quantity=cart_product.quantity,
                price=cart_product.product.price
            )
        
        cart_products.delete()
        messages.success(request, f"Siparişiniz başarıyla oluşturuldu! Sipariş numarası: #{order.id}")
        return redirect('order_detail', order_id=order.id)
    
    # GET request - checkout sayfasını göster
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    cart_products = CartProduct.objects.filter(user=request.user)
    
    if not cart_products.exists():
        messages.error(request, "Sepetinizde ürün bulunmamaktadır!")
        return redirect('cart')
    
    total_amount = sum(product.product.price * product.quantity for product in cart_products)
    total_amount += 29.99  # Kargo ücreti
    
    context = {
        'addresses': addresses,
        'cart_products': cart_products,
        'total_amount': total_amount,
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Sipariş bulunamadı!")
        return redirect('profile')
    
    context = {
        'order': order,
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'order_detail.html', context)

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    
    context = {
        'orders': orders,
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'order_history.html', context)

@login_required(login_url='login')
def address_list(request):
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    context = {
        'addresses': addresses,
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'address_list.html', context)

@login_required(login_url='login')
def add_address(request):
    if request.method == "POST":
        title = request.POST.get('title')
        address_type = request.POST.get('address_type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        district = request.POST.get('district')
        neighborhood = request.POST.get('neighborhood')
        address = request.POST.get('address')
        is_default = request.POST.get('is_default') == 'on'
        
        new_address = Address.objects.create(
            user=request.user,
            title=title,
            address_type=address_type,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            city=city,
            district=district,
            neighborhood=neighborhood,
            address=address,
            is_default=is_default
        )
        
        messages.success(request, "Adres başarıyla eklendi!")
        return redirect('address_list')
    
    context = {
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'add_address.html', context)

@login_required(login_url='login')
def edit_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        messages.error(request, "Adres bulunamadı!")
        return redirect('address_list')
    
    if request.method == "POST":
        address.title = request.POST.get('title')
        address.address_type = request.POST.get('address_type')
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.phone = request.POST.get('phone')
        address.city = request.POST.get('city')
        address.district = request.POST.get('district')
        address.neighborhood = request.POST.get('neighborhood')
        address.address = request.POST.get('address')
        address.is_default = request.POST.get('is_default') == 'on'
        address.save()
        
        messages.success(request, "Adres başarıyla güncellendi!")
        return redirect('address_list')
    
    context = {
        'address': address,
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'edit_address.html', context)

@login_required(login_url='login')
def delete_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        address.delete()
        messages.success(request, "Adres başarıyla silindi!")
    except Address.DoesNotExist:
        messages.error(request, "Adres bulunamadı!")
    
    return redirect('address_list')

@login_required(login_url='login')
def set_default_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        # Diğer adresleri varsayılan olmaktan çıkar
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        # Bu adresi varsayılan yap
        address.is_default = True
        address.save()
        messages.success(request, "Varsayılan adres güncellendi!")
    except Address.DoesNotExist:
        messages.error(request, "Adres bulunamadı!")
    
    return redirect('address_list')

@login_required(login_url='login')
def track_shipment(request):
    if request.method == "POST":
        tracking_number = request.POST.get('tracking_number')
        if tracking_number:
            try:
                order = Order.objects.get(tracking_number=tracking_number, user=request.user)
                if order.status == 'shipped':
                    import random
                    import json
                    
                    lat = random.uniform(36.0, 42.0)
                    lng = random.uniform(26.0, 45.0)
                    
                    shipment_data = {
                        'tracking_number': tracking_number,
                        'status': order.get_status_display(),
                        'current_location': {
                            'lat': lat,
                            'lng': lng,
                            'address': f"Kargo Merkezi - {random.choice(['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya'])}"
                        },
                        'estimated_delivery': '2-3 iş günü',
                        'last_update': order.order_date.strftime('%d.%m.%Y %H:%M'),
                        'route': [
                            {'lat': 41.0082, 'lng': 28.9784, 'name': 'İstanbul Dağıtım Merkezi'},
                            {'lat': lat, 'lng': lng, 'name': 'Yolda'},
                            {'lat': 39.9334, 'lng': 32.8597, 'name': 'Teslimat Adresi'}
                        ]
                    }
                    
                    context = {
                        'shipment_data': json.dumps(shipment_data),
                        'order': order,
                        'product_quantity': ProductQuantity(request),
                    }
                    return render(request, 'track_shipment.html', context)
                else:
                    messages.error(request, "Bu kargo henüz yola çıkmamış!")
                    return redirect('track_shipment')
            except Order.DoesNotExist:
                messages.error(request, "Kargo takip numarası bulunamadı!")
                return redirect('track_shipment')
    
    context = {
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'track_shipment.html', context)

@login_required(login_url='login')
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating', 5)
        
        # Kullanıcının bu ürünü satın alıp almadığını kontrol et
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered'
        ).exists()
        
        if not has_purchased:
            messages.error(request, 'Bu ürünü satın almadığınız için yorum yapamazsınız.')
            return redirect('product_detail', product_id=product_id)
        
        # Kullanıcının bu ürün için daha önce yorum yapıp yapmadığını kontrol et
        existing_comment = Comment.objects.filter(user=request.user, product=product).first()
        if existing_comment:
            messages.error(request, 'Bu ürün için zaten yorum yapmışsınız.')
            return redirect('product_detail', product_id=product_id)
        
        Comment.objects.create(
            user=request.user,
            product=product,
            comment=comment_text,
            rating=int(rating),
            is_verified_purchase=True
        )
        
        messages.success(request, 'Yorumunuz başarıyla eklendi.')
        return redirect('product_detail', product_id=product_id)
    
    return redirect('product_detail', product_id=product_id)

@login_required(login_url='login')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating', 5)
        
        comment.comment = comment_text
        comment.rating = int(rating)
        comment.save()
        
        messages.success(request, 'Yorumunuz başarıyla güncellendi.')
        return redirect('product_detail', product_id=comment.product.id)
    
    context = {
        'comment': comment,
        'product_quantity': ProductQuantity(request),
    }
    return render(request, 'edit_comment.html', context)

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    product_id = comment.product.id
    comment.delete()
    
    messages.success(request, 'Yorumunuz başarıyla silindi.')
    return redirect('product_detail', product_id=product_id)

def get_product_comments(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product).order_by('-create_date')
    
    comment_data = []
    for comment in comments:
        comment_data.append({
            'id': comment.id,
            'user': comment.user.username,
            'comment': comment.comment,
            'rating': comment.rating,
            'create_date': comment.create_date.strftime('%d.%m.%Y'),
            'is_verified_purchase': comment.is_verified_purchase,
            'can_edit': request.user == comment.user,
        })
    
    return JsonResponse({'comments': comment_data})

