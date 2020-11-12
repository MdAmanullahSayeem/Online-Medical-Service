from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Account, Message
from .forms import MessageForm, MsgForm, MsgFileForm, MsgPicForm
from myapp import views
from django.contrib.auth.models import User
from django.db.models import Q
import os
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required

@login_required(login_url='/myapp/user/login/')
def msg_send(request):
    template_data = views.parse_session(request, {'form_button': "send"})
    default = {}
    default['sender'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = MessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            obj = Message(
                sender=form.cleaned_data['sender'].user,
                receiver=form.cleaned_data['receiver'].user,
                message=form.cleaned_data['message'],
            )
            obj.save()
            return HttpResponseRedirect('/myapp/message/receive/')

    else:
        form._errors = {}
    form.disable_field('sender')
    template_data['form'] = form
    return render(request, 'myapp/message/send.html', template_data)


@login_required(login_url='/myapp/user/login/')
def msg_receive(request):
    query = Message.objects.all().filter(receiver=request.user).order_by('-timestamp')

# as mysql doesn't support distinct query following process can pass distinct value to query

    copy1 = []
    copy2 = []
    for data in query:
        if data.sender.pk not in copy1:
            copy1.append(data.sender.pk)
            copy2.append(data)
    obj = copy2

    return render(request, 'myapp/message/receive.html', {'bus': obj})


@login_required(login_url='/myapp/user/login/')
def recent_msg(request, sender, receiver):
    obj = Message.objects.all().filter(sender=sender, receiver=receiver)
    return render(request, 'myapp/message/msg.html', {'bus': obj})


@login_required(login_url='/myapp/user/login/')
def messenger(request, ck=None):
    pk = request.GET['pk']
    request.POST._mutable = True
    user=User.objects.get(pk=pk)
    data = Message.objects.all().filter(sender=user, receiver=request.user)
    try:
        for x in data:
            if x.read==False:
                x.read = True
                x.save()

    except:
        pass
    sender = request.user.pk
    receiver = User.objects.get(pk=pk)
    obj = Message.objects.all().filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
    template_data = views.parse_session(request, {'form_button': "send", 'form_action': ck + "?pk=" + pk, 'bus': obj, 'sender': pk})

    if request.method == 'POST':
        if ck == 'b':
            form = MsgFileForm(request.POST, request.FILES)
        elif ck == 'c':
            form = MsgPicForm(request.POST, request.FILES)
        else:
            form = MsgForm(request.POST, request.FILES)
        if form.is_valid():
            if ck == 'b':
                obj = Message(sender=request.user, receiver=receiver, file=form.cleaned_data['msg'], )
            elif ck == 'c':
                obj = Message(sender=request.user, receiver=receiver, pic=form.cleaned_data['msg'], )
            else:
                obj = Message(sender=request.user, receiver=receiver, message=form.cleaned_data['msg'],)
            obj.save()
            print('all saved')
            return HttpResponseRedirect('/myapp/message/messenger/a?pk='+pk)
    else:
        recent_msg(request, sender, receiver)
        if ck == 'b':
            form = MsgFileForm()
        elif ck == 'c':
            form = MsgPicForm()
        else:
            form = MsgForm
    template_data['form'] = form

    return render(request, 'myapp/message/messenger.html', template_data)



def file_response_download(request, file_path):
    ext = os.path.basename(file_path).split('.')[-1].lower()
    # cannot be used to download py, db and sqlite3 files.
    if ext not in ['py', 'db',  'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        raise Http404
