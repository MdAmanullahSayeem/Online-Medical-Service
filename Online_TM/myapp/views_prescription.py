import os

from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .forms import PresForm
from .models import Account,Prescription
from myapp import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/myapp/user/login/')
def pres_create(request):
    template_data = views.parse_session(request, {'form_button':"Add Prescription"})
    default = {}
    if request.user.account.role == Account.DOCTOR:
        default['doctor'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = PresForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            pres=Prescription(
                doctor=form.cleaned_data['doctor'].user,
                patient=form.cleaned_data['patient'].user,
                date=form.cleaned_data['date'],
                age=form.cleaned_data['age'],
                medications=form.cleaned_data['medications'],
            )
            pres.save()
            messages.success(request,'Prescription created')
            return HttpResponseRedirect('/myapp/pres/list/')

    else:
        form._errors = {}
    if request.user.account.role == Account.DOCTOR:
        form.disable_field('doctor')
    template_data['form'] = form
    return render(request, 'myapp/prescription/create.html', template_data)

@login_required(login_url='/myapp/user/login/')
def pres_list(request):
    if request.user.account.role == 'PA':
        query = Prescription.objects.all().filter(patient=request.user)
    if request.user.account.role == 'DOC':
        query = Prescription.objects.all().filter(doctor=request.user)
    return render(request, 'myapp/prescription/list.html', {'query': query})


@login_required(login_url='/myapp/user/login/')
def pres_view(request, pk=None):
    obj = Prescription.objects.get(pk=pk)
    obj.read = True
    obj.save()
    request.session['pk']=pk
    return render(request, 'myapp/prescription/view.html', {'bus':obj})


@login_required(login_url='/myapp/user/login/')
def pres_cancel(request, pk=None):
    obj = Prescription.objects.get(pk=pk)
    obj.delete()
    messages.success(request, 'prescription Canceled')
    return HttpResponseRedirect('/myapp/pres/list/')

