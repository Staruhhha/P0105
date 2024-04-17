from django.db import models

MAX_LENGTH = 100

class Manufacturer(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    address = models.CharField(max_length=MAX_LENGTH, verbose_name='Адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Supply(models.Model):
    date = models.DateTimeField(verbose_name='Дата')

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, verbose_name='Производитель')
    products = models.ManyToManyField('Product', through='Pos_supply', verbose_name='Товары')

    def __str__(self):
        return f"Поставка №{self.pk}: {self.date}, {self.manufacturer.name}"

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'


class Pos_supply(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Товар')
    supply = models.ForeignKey(Supply, on_delete=models.PROTECT, verbose_name='Поставка')

    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'Позиция поставки'
        verbose_name_plural = 'Позиции поставок'


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Order(models.Model):
    SHOP = "SH"
    COURIER = "CR"
    PICKUPPOINT = "PP"

    TYPE_DELIVERY = [
        (SHOP, "Магазин"),
        (COURIER, "Курьер"),
        (PICKUPPOINT, "Пункт выдачи"),
    ]

    customer_surname = models.CharField(max_length=MAX_LENGTH, verbose_name='Фамилия покупателя')
    customer_name = models.CharField(max_length=MAX_LENGTH, verbose_name='Имя покупателя')
    customer_patronymic = models.CharField(max_length=MAX_LENGTH, verbose_name='Отчество покупателя', null=True, blank=True)
    delivery_address = models.CharField(max_length=MAX_LENGTH, verbose_name='Адрес')
    delivery_type = models.CharField(max_length=2, choices=TYPE_DELIVERY, default=SHOP, verbose_name='Тип доставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')

    products = models.ManyToManyField('Product', through='Pos_order', verbose_name='Товары')

    def __str__(self):
        return f"Заказ №{self.pk}: {self.created_at}, {self.customer_surname} {self.customer_name} {self.customer_patronymic}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Pos_order(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'


class Parameter(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

class Pos_parameter(models.Model):
    parameter = models.ForeignKey('Parameter', on_delete=models.PROTECT, verbose_name='Характеристика')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Товар')
    value = models.CharField(max_length=MAX_LENGTH, verbose_name='Значение')

    def __str__(self):
        return f"{self.product.name}: {self.parameter.name} - {self.value}"

    class Meta:
        verbose_name = 'Позиция характеристики'
        verbose_name_plural = 'Позиции характеристик'


class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='Картинка', blank=True, null=True)
    available_to_purchase = models.BooleanField(default=True, verbose_name='Есть в наличии')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    parameters = models.ManyToManyField(Parameter, through=Pos_parameter)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'