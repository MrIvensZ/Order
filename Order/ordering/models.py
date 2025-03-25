from django.db import models
from .validators import validate_table_available


class Dish(models.Model):
    "Модель для блюд"

    name = models.CharField(max_length=100,
                            verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class OrderItem(models.Model):
    "Промежуточная модель для хранения количества блюд в заказах"

    dish = models.ForeignKey(Dish,
                             on_delete=models.CASCADE,
                             verbose_name='Блюдо')
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              verbose_name='Заказ')
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Количество')

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.dish.price * self.quantity


class Order(models.Model):
    "Модель заказа"

    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField(validators=[validate_table_available,],
                                       verbose_name='Номер стола')
    dishes = models.ManyToManyField(Dish,
                                    through=OrderItem,
                                    verbose_name='Блюда')
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='waiting',
                              verbose_name='Статус')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table_number})"

    @property
    def total_price(self):
        "Вычисление общей стоимости заказа"

        return sum(item.total_price for item in self.orderitem_set.all())
