from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

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
    adress, created = Adress.objects.get_or_create(user=user)

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
    error_message = None
    edit_comment = None

    # Favori kontrolü
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    if request.method == "POST":
        if request.POST.get("productid"):
            productid = request.POST.get("productid")
            product = Product.objects.get(id=productid)
            quantity = int(request.POST.get("quantity", 1))
            cart_product, created = CartProduct.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_product.quantity += quantity
            else:
                cart_product.quantity = quantity
            cart_product.save()
        elif request.POST.get("comment"):
            comment_text = request.POST.get("comment_text")
            if request.user.is_authenticated and comment_text:
                # Kullanıcı bu ürüne daha önce yorum yapmış mı kontrol et
                if not Comment.objects.filter(user=request.user, product=product).exists():
                    Comment.objects.create(
                        user=request.user,
                        comment=comment_text,
                        product=product
                    )
                    return redirect('product_detail', product_id=product.id)
                else:
                    error_message = "Bu ürüne zaten bir yorum yaptınız."
        elif request.POST.get("edit_comment_id"):
            edit_comment_id = request.POST.get("edit_comment_id")
            edit_comment_text = request.POST.get("edit_comment_text")
            try:
                comment_obj = Comment.objects.get(id=edit_comment_id, user=request.user, product=product)
                comment_obj.comment = edit_comment_text
                comment_obj.save()
                return redirect('product_detail', product_id=product.id)
            except Comment.DoesNotExist:
                error_message = "Yorumu düzenleme yetkiniz yok."
        elif request.POST.get("edit_request_id"):
            # Düzenleme formunu göstermek için
            try:
                edit_comment = Comment.objects.get(id=request.POST.get("edit_request_id"), user=request.user, product=product)
            except Comment.DoesNotExist:
                edit_comment = None

    context = {
        'product': product,
        'product_quantity': ProductQuantity(request),
        'comments': comments,
        'error_message': error_message,
        'edit_comment': edit_comment,
        'is_favorite': is_favorite,
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

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=email, first_name=first_name,last_name=last_name,email=email, password=password)
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Bu E-Posta Adresi Kayıtlı Değil")

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