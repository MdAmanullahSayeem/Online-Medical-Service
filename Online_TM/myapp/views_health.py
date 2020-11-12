from django.shortcuts import render, HttpResponseRedirect, redirect
from .views import parse_session
from .forms import HealthForm, FileForm, DocFrom
from .models import Health, DocProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def qualification_create(request):
    if not DocProfile.objects.filter(user=request.user).count():
        DocProfile.objects.create(user=request.user)
        messages.success(request, 'added success')
    return redirect('qualification_view')


@login_required(login_url='/myapp/user/login/')
def qualification_update(request):
    pk = request.user.pk
    # Authentication check.
    doc = DocProfile.objects.get(user=pk)
    # Get the template data from the session
    template_data = parse_session(request, {'form_button': "Update"})
    request.POST._mutable = True
    request.POST['user'] = request.user.account.pk
    if request.method == 'POST':
        form = DocFrom(request.POST, request.FILES)
        if form.is_valid():
            form.assign(doc)
            doc.save()
            messages.success(request, 'Your profile updated')
            template_data['form'] = form
            request.session['pk']=pk
            return redirect('qualification_view')
    else:
        form = DocFrom(doc.get_existed_data())
    form.disable_field('user')
    template_data['form'] = form
    return render(request, 'myapp/health/qualification_update.html', template_data)


@login_required(login_url='/myapp/user/login/')
def qualification_view(request):
    try:
        pk = request.GET['pk']
    except:
        pk = request.session['pk']
    try:
        query = DocProfile.objects.get(user=pk)
    except:
        query =None
    return render(request, 'myapp/health/qualification_view.html', {'query': query})


@login_required(login_url='/myapp/user/login/')
def health_create(request):
    if not Health.objects.filter(user=request.user).count():
        Health.objects.create(user=request.user)
        messages.success(request, 'added success')
    return redirect('health_view')



@login_required(login_url='/myapp/user/login/')
def health_update(request):
    pk = request.user.pk
    # Authentication check.
    health = Health.objects.get(user=pk)
    # Get the template data from the session
    template_data = parse_session(request, {'form_button': "Update"})
    request.POST._mutable = True
    request.POST['user'] = request.user.account.pk
    if request.method == 'POST':
        form = HealthForm(request.POST, request.FILES)
        if form.is_valid():
            form.assign(health)
            health.save()
            template_data['form'] = form
            request.session['pk']=pk
            messages.success(request, 'Your health updated')
            return redirect('health_view')
    else:
        form = HealthForm(health.get_existed_data())
    form.disable_field('user')
    template_data['form'] = form
    return render(request, 'myapp/health/health_update.html', template_data)


@login_required(login_url='/myapp/user/login/')
def health_view(request):
    try:
        pk = request.GET['pk']
    except:
        pk = request.session['pk']
    try:
        query = Health.objects.get(user=pk)
    except:
        query =None
    return render(request, 'myapp/health/health_view.html', {'query': query})




@login_required(login_url='/myapp/user/login/')
def t_report_cancel(request):
    health = Health.objects.get(user=request.user)
    health.T_report = None
    health.save()
    request.session['pk']=request.user.pk
    return HttpResponseRedirect('/myapp/user/profile/health/view/')

@login_required(login_url='/myapp/user/login/')
def t_report(request):
    template_data = parse_session(request, {'form_button': "Upload"})
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            health = Health.objects.get(user=request.user)
            health.T_report=form.cleaned_data['msg']
            health.save()
            messages.success(request, 'Your H_report updated')
            request.session['pk']=request.user.pk
            return HttpResponseRedirect('/myapp/user/profile/health/view/')

    else:
        form = FileForm()
    template_data['form'] = form
    return render(request, 'myapp/health/t_report.html', template_data)

#for both health and qualificaton
def simple_profile(request):
    try:
        pk = request.GET['pk']
    except:
        pk = request.session['pk']
    query=User.objects.get(pk=pk)
    return render(request, 'myapp/health/simple_profile.html', {'query':query})
