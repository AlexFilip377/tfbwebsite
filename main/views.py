from django.shortcuts import render, redirect
from .models import Client, Notification
from .forms import ClientRegistrationForm
from django.db.models import Q
from datetime import timedelta, datetime, date
from django.utils.timezone import now, make_aware
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required
def index(request):
    notifications_count = Notification.objects.filter(is_read=False).count()
    data = {
        'title': 'Работа с клиентами',
        'notifications_count': notifications_count
    }
    return render(request, 'main/index.html', data)

@login_required
def register(request):
    notifications_count = Notification.objects.filter(is_read=False).count()
    form = ClientRegistrationForm()

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент успешно зарегестрирован!')
            return redirect('register')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = ClientRegistrationForm()
        
    return render(request, 'main/register.html', {'form': form, 'notifications_count': notifications_count})

@login_required
def search(request):

    query = request.GET.get('search')
    results = None
    if query:
        results = Client.objects.filter(
            Q(name__icontains=query) | Q(membership_number__icontains=query) | Q(phone__icontains=query)
        )
        
    return render(request, 'main/search.html', {'results': results})


@login_required
def membership_list(request):
    notifications_count = Notification.objects.filter(is_read=False).count()
    query = request.GET.get('q')
    if query:
        memberships = Client.objects.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(membership_type__icontains=query) |
            Q(membership_number__icontains=query)
        )

    else:
        memberships = Client.objects.all()
    return render(request, 'main/membership_list.html', {'memberships': memberships, 'notifications_count': notifications_count})


@login_required
def notifications(request):
    notifications_count = Notification.objects.filter(is_read=False).count()
    
    create_notifications()
    notifications = Notification.objects.all().order_by('date_due')
    unread_count = notifications.count()
    
    print("Notifications:", notifications)
    
    notifications.update(read=True)
    
    return render(request, 'main/notifications.html', {'notifications': notifications, 'unread_count': unread_count,  'notifications_count': notifications_count})


def create_notifications():
    today = datetime.now().date()
    three_days_later = today + timedelta(days=3)

    clients_with_ending_subscriptions = Client.objects.filter(end_date__lte=three_days_later, end_date__gte=today)

    for client in clients_with_ending_subscriptions:
        date_due = make_aware(datetime.combine(client.end_date, datetime.min.time()))

        if not Notification.objects.filter(user=client.user, message__contains=f" у {client.name} заканчивается абонемент.", date_due=date_due).exists():
            Notification.objects.create(
                type='subscription_end',
                message=f"Через {(client.end_date - today).days} дня(дней) у {client.name} заканчивается абонемент.",
                user=client.user,
                date_due=date_due
            )

    birthday_today = Client.objects.filter(birthdate__month=today.month, birthdate__day=today.day)
    
    for client in birthday_today:
        if not Notification.objects.filter(user=client.user, message__contains=f"Сегодня день рождения у {client.name}!", date_due=today).exists():
            Notification.objects.create(
                type='birthday',
                message=f"Сегодня день рождения у {client.name}!",
                user=client.user,
                date_due=make_aware(datetime.combine(today, datetime.min.time()))
            )
        


def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success', 'message': 'Помеченно как прочитанное'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': "Не найдено"})
    

@login_required
def notification_view(request):
    notifications_count = Notification.objects.filter(is_read=False).count()
    return render(request, 'notification.html', {'notifications_count': notifications_count})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'main/login.html')