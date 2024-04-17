from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'address')
    list_display_links = ('__str__',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'manufact_name_info')
    list_display_links = ('id', 'date',)
    list_filter = ('manufacturer__name',)
    ordering = ('-date',)

    @admin.display(description='Производитель')
    def manufact_name_info(self, obj):
        return f"{obj.manufacturer.name}"


@admin.register(Pos_supply)
class Pos_supplyAdmin(admin.ModelAdmin):
    list_display = ('supply', 'product', 'quantity')
    list_display_links = None
    list_editable = ('supply', 'product', 'quantity')
    list_filter = ('supply',)
    ordering = ('-supply__date',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'FIO_customer', 'delivery_address', 'delivery_type', 'created_at', 'finished_at')
    list_display_links = ('id', 'FIO_customer')
    search_fields = ('customer_surname', 'customer_name', 'customer_patronymic', 'delivery_address')
    list_editable = ('delivery_address', 'delivery_type', 'finished_at')
    list_filter = ('delivery_type',)
    ordering = ('-created_at',)

    @admin.display(description='ФИО покупателя')
    def FIO_customer(self, obj):
        if obj.customer_patronymic:
            return f"{obj.customer_surname} {obj.customer_name[0]}. {obj.customer_patronymic[0]}"
        return f'{obj.customer_surname} {obj.customer_name[0]}.'

@admin.register(Pos_order)
class Pos_orderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'discount')
    list_display_links = None
    search_fields = ('product__name', 'order__customer_firstname', 'order__customer_name', 'order__customer_patronymic')
    list_editable = ('order', 'product', 'quantity', 'discount')



@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ('name',)


@admin.register(Pos_parameter)
class Pos_parameterAdmin(admin.ModelAdmin):
    list_display = ('product', 'parameter', 'value')
    list_display_links = None
    list_editable = ('product', 'parameter', 'value')
    list_filter = ('parameter',)
    ordering = ('-product__name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available_to_purchase')
    list_display_links = ('name',)
    list_editable = ('price', 'available_to_purchase')
    list_filter = ('category__name', 'tags__name')
    ordering = ('-created_at',)