from django.shortcuts import render, HttpResponseRedirect
from myapp.views import parse_session
from .models import Password
from .forms import PassChangeForm, PasswordForm, EmailForm, ConfirmForm
from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
# Create your views here.
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    return render(request, 'myapp/base.html')

@login_required(login_url='/myapp/user/login/')
def password(request):
    template_data = parse_session(request, {'form_button': "Go"})
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        data = request.POST['password']
        ck = check_password(data, request.user.password)
        if ck is True:
            request.session['code']=request.user.password
            return HttpResponseRedirect('/myapp/password/change/')
        else:
            messages.success(request, 'Password is invalid')
    else:
        form = PasswordForm()
    template_data['form'] = form
    return render(request, 'myapp/password/confirm.html', template_data)

def pass_change(request):
    try:
        code = request.session['code']
        if request.user.password != code:
            messages.success(request, 'Permission Denied')
            return HttpResponseRedirect('/myapp/password/')
    except:
        messages.success(request, 'Permission Denied')
        return HttpResponseRedirect('/myapp/password/')
    template_data = parse_session(request, {'form_button': "Password change"})
    if request.method == 'POST':
        form = PassChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            messages.success(request, 'Password changed successfully')
            login(request, user)
            return HttpResponseRedirect('/myapp/user/profile/')
    else:
        form = PassChangeForm()
    template_data['form'] = form
    return render(request, 'myapp/password/change.html', template_data)


from django.conf import settings
from django.core import mail
from django.views.generic.base import View
from django.template.loader import render_to_string
connection = mail.get_connection()

# Manually open the connection
connection.close()


def send_mail(receiver, code):
    code=code
    template = render_to_string('myapp/password/text.html')
    email = mail.EmailMessage(
        'account_reset',
        template,
        settings.EMAIL_HOST_USER,
        [receiver],
        connection=connection,
    )
    email.send()


def validate_code(email):
    query = Password.objects.filter(email=email).order_by('-timestamp')[0]
    if timezone.now().minute - query.timestamp.minute < 1:
        return True
    else:
        return False


def set_view_done(request):
    email = request.session['email']
    template_data = parse_session(request, {'form_button': "Password change"})
    if request.method == 'POST':
        form = PassChangeForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=email)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            messages.success(request, 'password changed successfully')
            login(request, user)
            Password.objects.all().filter(email=email).delete()
            return HttpResponseRedirect('/user/profile/')
    else:
        form = PassChangeForm()
    template_data['form'] = form
    return render(request, 'myapp/password/change.html', template_data)


def set_view_confirm(request):
    email = request.session['email']
    template_data = parse_session(request, {'form_button': "submit"})
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            validate = validate_code(email)
            if validate is True:
                recover = Password.objects.filter(email=email).order_by('-timestamp')[0]
                code2 = recover.code
                if code == code2:
                    request.session['email'] = email
                    return HttpResponseRedirect('/myapp/set/view/done/')
                else:
                    messages.success(request, 'Wrong Code')
            else:
                messages.success(request, 'Session Expire , enter email again')
                return HttpResponseRedirect('/myapp/set/view/')
    else:
        form = ConfirmForm()
    template_data['form'] = form
    return render(request, 'myapp/password/confirm/view.html', template_data)


def set_view(request):
    template_data = parse_session(request, {'form_button': "go"})
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            code = get_random_string(length=6)
            store = Password(
                email=email,
                code=code
            )
            store.save()

            messages.success(request, 'a code sent to your email, enter the code bellow')
            return HttpResponseRedirect('/myapp/set/view/confirm/')
    else:
        form = EmailForm()
    template_data['form'] = form
    return render(request, 'myapp/password/reset/view.html', template_data)