from django.http import HttpRequest, HttpResponseBadRequest
from .forms import PartnerForm
from .forms import AnketaForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth import login as auth_login, authenticate

from .models import Partner, Comment


# Create your views here.

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def auth_page(request):
    """Страница для входа и регистрации пользователей."""
    assert isinstance(request, HttpRequest)

    login_errors = None
    reg_errors = None

    if request.method == "POST":
        if 'login' in request.POST:
            # Обработка формы входа
            login_form = AuthenticationForm(request, data=request.POST)
            reg_form = CustomUserCreationForm()  # используем кастомную форму
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('home')
            else:
                login_errors = login_form.errors
        elif 'register' in request.POST:
            # Обработка формы регистрации
            reg_form = CustomUserCreationForm(request.POST)  # используем кастомную форму
            login_form = AuthenticationForm()  # оставляем форму входа пустой
            if reg_form.is_valid():
                user = reg_form.save(commit=False)
                user.is_active = True
                user.is_staff = False
                user.is_superuser = False
                user.date_joined = datetime.now()
                user.last_login = datetime.now()
                user.save()
                # Автоматический вход после регистрации (опционально)
                user = authenticate(username=reg_form.cleaned_data.get('username'),
                                    password=reg_form.cleaned_data.get('password1'))
                if user is not None:
                    auth_login(request, user)
                return redirect('home')
            else:
                reg_errors = reg_form.errors
    else:
        login_form = AuthenticationForm()
        reg_form = CustomUserCreationForm()  # используем кастомную форму

    context = {
        'login_form': login_form,
        'reg_form': reg_form,
        'login_errors': login_errors,
        'reg_errors': reg_errors,
        'year': datetime.now().year,
    }
    return render(request, 'auth.html', context)

def links(request):
    return render(request, 'links.html')
def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    internet = {'1': 'Плохо', '2': 'Средне',
                '3': 'Хорошо', '4': 'Отлично'}

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['internet'] = internet[form.cleaned_data['internet']]
            if form.cleaned_data['notice'] == True:
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()

    return render(
        request,
        'anketa.html',
        {
            'form': form,
            'data': data
        }
    )
def partner_list(request):
    partners = Partner.objects.all()
    return render(request, 'partner_list.html', {'partners': partners})

def partner_detail(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    comments = Comment.objects.filter(partner=partner)  # Загружаем только нужные комментарии
    return render(request, 'partner_detail.html', {'partner': partner, 'comments': comments})
def partner_comment(request, pk):
    if request.method == "POST":
        partner = get_object_or_404(Partner, pk=pk)
        text = request.POST.get("comment")
        if not text.strip():
            return HttpResponseBadRequest("Комментарий не может быть пустым")
        Comment.objects.create(partner=partner, text=text, author="Аноним")
        return redirect("partner_detail", pk=pk)  # Редирект на страницу партнёра
    return None

def add_partner(request):
    if request.method == "POST":
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('partner_list')  # Перенаправляем на список партнёров после успешного создания
    else:
        form = PartnerForm()

    return render(request, 'add_partner.html', {'form': form})
def video(request):
    return render(request, 'video.html')
def cbutton(request):
    return render(request, 'cotton/button.html')