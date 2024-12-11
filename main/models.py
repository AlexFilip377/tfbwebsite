from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    name = models.CharField('Имя Клиента', max_length=100)
    phone = models.CharField('Номер телефона', max_length=20)
    email = models.EmailField('Email', blank=True, null=True)
    membership_number = models.CharField('Номер абонемента', max_length=50, unique=True)
    birthdate = models.DateField('Дата рождения', blank=True, null=True)
    membership_type = models.CharField('Вид абонемента', max_length=50)
    membership_price = models.DecimalField('Цена абонемента', max_digits=8, decimal_places=2)
    payment_method = models.CharField('Способ оплаты', max_length=50)
    start_date = models.DateField('Начало действия абонемента')
    end_date = models.DateField('Конец действия абонемента')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Notification(models.Model):
    NOTIFY_TYPE_CHOICES = [
        ('subscription_end', 'Окончание абонемента'),
        ('birthday', 'День рождения')
    ]

    type = models.CharField(max_length=50, choices=NOTIFY_TYPE_CHOICES)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField()
    read = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message
    
    def is_due(self):
        return self.data_due <= timezone.now()