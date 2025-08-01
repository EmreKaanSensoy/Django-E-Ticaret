from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']
    ordering = ['order']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'price', 'stock', 'stock_status', 'is_in_stock', 'gender', 'color', 'image_count']
    list_filter = ['brand', 'gender', 'color', 'case_shape', 'strap_type', 'stock']
    search_fields = ['brand__brand', 'model', 'description']
    ordering = ['brand', 'model']
    inlines = [ProductImageInline]
    list_editable = ['stock']
    actions = ['update_stock_status']
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Görsel Sayısı'
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return "Stokta Yok"
        elif obj.stock <= 5:
            return f"Son {obj.stock} Adet"
        else:
            return "Stokta Var"
    stock_status.short_description = 'Stok Durumu'
    
    def is_in_stock(self, obj):
        return obj.is_in_stock
    is_in_stock.boolean = True
    is_in_stock.short_description = 'Stokta Var'
    
    def update_stock_status(self, request, queryset):
        updated_count = 0
        for product in queryset:
            if product.stock == 0:
                product.stock = 10  # Örnek: Stok ekle
                product.save()
                updated_count += 1
        
        self.message_user(request, f"{updated_count} ürünün stok durumu güncellendi.")
    update_stock_status.short_description = "Seçili ürünlere stok ekle"

admin.site.register(CartProduct)
admin.site.register(Profile)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__model', 'alt_text']
    ordering = ['product', 'order']
    list_editable = ['order', 'is_primary']
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'first_name', 'last_name', 'city', 'district', 'is_default']
    list_filter = ['address_type', 'is_default', 'city']
    search_fields = ['user__username', 'first_name', 'last_name', 'city']
    ordering = ['user', '-is_default']


admin.site.register(Favorite)
admin.site.register(Comment)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand']
    search_fields = ['brand']
    ordering = ['brand']

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['gender']
    search_fields = ['gender']
    ordering = ['gender']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color']
    search_fields = ['color']
    ordering = ['color']

@admin.register(CaseShape)
class CaseShapeAdmin(admin.ModelAdmin):
    list_display = ['case_shape']
    search_fields = ['case_shape']
    ordering = ['case_shape']

@admin.register(StrapType)
class StrapTypeAdmin(admin.ModelAdmin):
    list_display = ['strap_type']
    search_fields = ['strap_type']
    ordering = ['strap_type']

@admin.register(GlassFeature)
class GlassFeatureAdmin(admin.ModelAdmin):
    list_display = ['glass_feature']
    search_fields = ['glass_feature']
    ordering = ['glass_feature']

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ['style']
    search_fields = ['style']
    ordering = ['style']

@admin.register(Mechanism)
class MechanismAdmin(admin.ModelAdmin):
    list_display = ['mechanism']
    search_fields = ['mechanism']
    ordering = ['mechanism']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'total_amount', 'status', 'can_cancel']
    list_filter = ['status', 'order_date']
    search_fields = ['user__username', 'user__email', 'id']
    readonly_fields = ['order_date']
    ordering = ['-order_date']
    actions = ['cancel_selected_orders']
    
    def can_cancel(self, obj):
        return obj.can_cancel()
    can_cancel.boolean = True
    can_cancel.short_description = 'İptal Edilebilir'
    
    def cancel_selected_orders(self, request, queryset):
        cancelled_count = 0
        for order in queryset:
            if order.cancel_order():
                cancelled_count += 1
        
        self.message_user(request, f"{cancelled_count} sipariş başarıyla iptal edildi.")
    cancel_selected_orders.short_description = "Seçili siparişleri iptal et"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__status']
    search_fields = ['order__id', 'product__model']

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'is_verified', 'is_expired']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['token', 'created_at']
    ordering = ['-created_at']
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Süresi Dolmuş'