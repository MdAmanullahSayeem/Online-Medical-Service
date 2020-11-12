from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.http import HttpResponse
from .forms import SignipUPform, LoginForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
import csv
from django.http import FileResponse


def parse_session(request, template_data=None):

    if template_data is None:
        template_data = {}
    if request.session.has_key('alert_success'):
        template_data['alert_success'] = request.session.get('alert_success')
        del request.session['alert_success']
    if request.session.has_key('alert_danger'):
        template_data['alert_danger'] = request.session.get('alert_danger')
        del request.session['alert_danger']
    return template_data


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def home(request):
    return render(request, 'myapp/base.html')


def login_view(request):
    # Authentication check. Users currently logged in cannot view this page.
    if request.user.is_authenticated:
        return HttpResponseRedirect('/myapp/user/profile/')
    # Get the template data from the session
    template_data = parse_session(request, {'form_button': "Login"})
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'].lower(),  # Make sure it's lowercase
                password=form.cleaned_data['password']
            )
            login(request, user)
            if request.user.is_authenticated:
                return HttpResponseRedirect("/myapp/user/profile")
    else:
        form = LoginForm()
    template_data['form'] = form
    return render(request, 'myapp/login.html', template_data)


def register(request):
    # Authentication check. Users logged in cannot view this page.
    # Get the template data from the session
    template_data = parse_session(request, {'form_button': "Register"})
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = SignipUPform(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'].lower(),  # Username, make sure it's lowercase
                form.cleaned_data['email'],  # Email
                form.cleaned_data['password1']  # Password
            )
            profile = user.profile
            profile.phone = form.cleaned_data['phone']
            profile.save()

            user = authenticate(
                username=form.cleaned_data['username'].lower(),  # Make sure it's lowercase
                password=form.cleaned_data['password1']
            )
            login(request,user)
            return HttpResponseRedirect("/myapp/user/profile")
    else:
        form = SignipUPform()
    template_data['form'] = form
    return render(request, 'myapp/form.html', template_data)


def mail(request):
    subject = "Greetings"
    msg = "hello check check"
    frm = "amaullahssayeem@gmail.com"
    to = "nayeemllb0@gmail.com"
    res = send_mail(subject, msg, frm, [to])
    if (res == 1):
        msg = "Mail Sent Successfuly"
    else:
        msg = "Mail could not sent"
    return HttpResponse(msg)



def getfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file3.csv"'
    employees = User.objects.all()
    writer = csv.writer(response)
    for employee in employees:
        writer.writerow([employee.username, employee.email])
    return response

def search_view(request):
    data = request.GET['data']
    if data !="":
        query = User.objects.filter(username__startswith=data)
        return render(request, 'myapp/search/search.html',{'query':query})
    else:
        messages.success(request,'Enter a string')
        return HttpResponseRedirect('/')


def practice(request):
    return render(request, 'unicode.html')