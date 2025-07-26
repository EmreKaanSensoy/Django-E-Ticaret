from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']
    ordering = ['order']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'price', 'gender', 'color', 'image_count']
    list_filter = ['brand', 'gender', 'color', 'case_shape', 'strap_type']
    search_fields = ['brand__brand', 'model', 'description']
    ordering = ['brand', 'model']
    inlines = [ProductImageInline]
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Görsel Sayısı'

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
    list_display = ['id', 'user', 'order_date', 'total_amount', 'status']
    list_filter = ['status', 'order_date']
    search_fields = ['user__username', 'user__email', 'id']
    readonly_fields = ['order_date']
    ordering = ['-order_date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__status']
    search_fields = ['order__id', 'product__model']