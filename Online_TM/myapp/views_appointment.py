from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from myapp import views
from myapp.models import Account, Appointment
from myapp.forms import AppointmentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='/myapp/user/login/')
def appointment_create(request):
    # Authentication check.
    template_data = views.parse_session(request, {'form_button': "Create"})
    # Proceed with the rest of the view
    default = {}
    if request.user.account.role == Account.PATIENT:
        default['patient'] = request.user.account.id
    elif request.user.account.role == Account.DOCTOR:
        default['doctor'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = AppointmentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = Appointment(
                doctor=form.cleaned_data['doctor'].user,
                patient=form.cleaned_data['patient'].user,
                date=form.cleaned_data['date'],
            )
            data.save()
            messages.success(request, 'Your appointment created')
            form = AppointmentForm(default)  # Clean the form when the page is redisplayed
            form._errors = {}
            return HttpResponseRedirect('/myapp/appointment/list/')

    else:
        form._errors = {}
    if request.user.account.role == Account.PATIENT:
        form.disable_field('patient')
    elif request.user.account.role == Account.DOCTOR:
        form.disable_field('doctor')
    template_data['form'] = form
    return render(request, 'myapp/appointment/create.html', template_data)


@login_required(login_url='/myapp/user/login/')
def appointment_list(request):
    if request.user.account.role == Account.PATIENT:
        query = Appointment.objects.filter(patient=request.user.id).order_by('-date')
    if request.user.account.role == Account.DOCTOR:
        query = Appointment.objects.filter(doctor=request.user.id).order_by('-date')
    return render(request, 'myapp/appointment/list.html', {'query': query})

@login_required(login_url='/myapp/user/login/')
def appointment_view(request, pk=None):
    obj = Appointment.objects.get(pk=pk)
    if request.user.account.role == 'DOC':
        try:
            if obj.read==False:
                obj.read=True
                obj.save()
        except:
            pass
    return render(request, 'myapp/appointment/view.html', {'bus': obj})


def active_list(request):
    query = Appointment.objects.filter(doctor=request.user.id, date=timezone.now())
    return render(request, 'myapp/appointment/active_list.html', {'query':query})


def activation(request, pk=None):
    obj = Appointment.objects.get(pk=pk)
    if obj.active == 1:
        Appointment.objects.filter(pk=pk).update(active=0)
        return HttpResponseRedirect('/myapp/appointment/list/')
    if obj.active == 0:
        Appointment.objects.filter(pk=pk).update(active=1)
        return HttpResponseRedirect('/myapp/appointment/list/')

    return render(request, 'myapp/appointment/view.html', {'bus':obj})


@login_required(login_url='/myapp/user/login/')
def appointment_cancel(request, pk=None):
    obj = Appointment.objects.get(pk=pk)
    obj.delete()
    messages.success(request, 'Your appointment canceled')
    return HttpResponseRedirect("/myapp/appointment/list/")


@login_required(login_url='/myapp/user/login/')
def update_view(request):
    pk = request.GET['pk']
    # Authentication check.
    appointment=Appointment.objects.get(pk=pk)
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Update", 'form_action': "?pk=" + pk})
    request.POST._mutable = True
    if request.user.account.role == Account.PATIENT:
        request.POST['patient'] = request.user.account.pk
    elif request.user.account.role == Account.DOCTOR:
        request.POST['doctor'] = request.user.account.pk

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.assign(appointment)
            appointment.save()
            template_data['form'] = form
            messages.success(request, 'Your appointment updated')
            return HttpResponseRedirect('/myapp/appointment/list/')

    else:
        form = AppointmentForm(appointment.get_existed_data())
    if request.user.account.role == Account.PATIENT:
        form.disable_field('patient')
    elif request.user.account.role == Account.DOCTOR:
        form.disable_field('doctor')

    template_data['form'] = form
    return render(request, 'myapp/appointment/update.html', template_data)
