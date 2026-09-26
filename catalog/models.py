from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Product(models.Model):
    TYPE_GAZEBO = "gazebo"
    TYPE_AVIARY = "aviary"

    TYPE_CHOICES = [
        (TYPE_GAZEBO, "Беседка"),
        (TYPE_AVIARY, "Вольер"),
    ]

    product_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Тип товара",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        verbose_name="URL-адрес",
    )

    main_image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Основное изображение",
    )

    short_description = models.CharField(
        max_length=300,
        verbose_name="Краткое описание",
    )

    description = models.TextField(
        verbose_name="Полное описание",
    )

    dimensions = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Размеры",
    )

    material = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Материал",
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Цена",
    )

    old_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Старая цена",
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Показывать на главной",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Показывать в каталоге",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "product_detail",
            kwargs={"slug": self.slug},
        )

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            discount = (
                (self.old_price - self.price)
                / self.old_price
                * 100
            )
            return round(discount)

        return 0


class RequestStatus(models.TextChoices):
    NEW = "new", "Новая"
    PROCESSING = "processing", "В обработке"
    CONTACTED = "contacted", "Клиенту позвонили"
    COMPLETED = "completed", "Завершена"
    CANCELLED = "cancelled", "Отменена"


class ProductRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="product_requests",
        verbose_name="Пользователь",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )

    phone = models.CharField(
        max_length=40,
        verbose_name="Телефон",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Электронная почта",
    )

    product_type = models.CharField(
        max_length=20,
        choices=Product.TYPE_CHOICES,
        verbose_name="Тип товара",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="requests",
        verbose_name="Выбранный товар",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )

    status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.NEW,
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата заявки",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка на товар"
        verbose_name_plural = "Заявки на товары"

    def __str__(self):
        return f"Заявка №{self.pk} — {self.name}"


class ConsultationRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="consultation_requests",
        verbose_name="Пользователь",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )

    phone = models.CharField(
        max_length=40,
        verbose_name="Телефон",
    )

    status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.NEW,
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата заявки",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультацию"

    def __str__(self):
        return f"Консультация №{self.pk} — {self.name}"