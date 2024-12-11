from django import forms
from .models import Client
import re
from django.contrib.auth.models import User

class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email', 'membership_number', 'birthdate',
                  'membership_type', 'membership_price', 'payment_method',
                  'start_date', 'end_date']
        
        widgets = {
            'membership_type': forms.Select(choices=[
                ('full', 'All day'),
                ('day', 'Дневной'),
                ('morning', 'Утренний'),
                ('evening', 'Вечерний'),
                ('kids', 'Детский'),
                ('one_time', 'Разовое посещение'),
            ]),
            'payment_method': forms.Select(choices=[
                ('cash', 'Наличные'),
                ('kaspi_qr', 'Kaspi QR'),
                ('kaspi_red', 'Kaspi red'),
                ('kaspi_transfer', 'Kaspi перевод'),
                ('halyk', 'Halyk'),
                ('card', 'Карта'),
                ('other', 'Другое'),
            ]),
        }
        
    birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?[0-9\s\-()]+$', phone):
            raise forms.ValidationError("Введите номер телефона в корректном формате.")
        return phone
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r'[\w\.-]+@[\w\.-]+\.\w{2,4}$', email):
            raise forms.ValidationError("Введите корректный адрес электронной почты.")
        return email

    def clean_membership_price(self):
        membership_price = self.cleaned_data.get('membership_price')
        if membership_price <= 0:
            raise forms.ValidationError("Укажите стоимость абонемента")
        return membership_price

    def clean_membership_number(self):
        membership_number = self.cleaned_data.get('membership_number')
        if len(membership_number) < 1:
            raise forms.ValidationError("Укажите номер абонемента")
        return membership_number