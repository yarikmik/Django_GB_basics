from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='имя',  # видимое имя
        max_length=64,
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True  # указывает на необязательность заполнения поля модели
    )

    # href = models.CharField(
    #     verbose_name='ссылка',  # видимое имя
    #     max_length=64,
    #     unique=True,
    #     default='#',
    # )

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):  # позволяет в админке выводить собственные имена объектов
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,  # первым параметром указываем модель с которой связываем
        on_delete=models.CASCADE,  # при удалении родителького объекта все связанные объекты так же удаляутся
        verbose_name='категория',
    )
    name = models.CharField(
        verbose_name='название продукта',
        max_length=128,
    )
    short_desc = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='краткое описание',
    )
    image = models.ImageField(
        upload_to='products_images',  # путь, куда сохранять изображение
        blank=True,
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )

    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,  # знаков после запятой,
        default=0,  # то что запишется в поле по умолчанию
    )

    quantity = models.PositiveIntegerField(  # PositiveIntegerField - неотрицательное целое число
        verbose_name='количество на складе',
        default=0,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - id_{self.category_id}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
