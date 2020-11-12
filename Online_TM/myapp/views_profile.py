from django.shortcuts import HttpResponseRedirect,render
from .views import parse_session
from .forms import ProfileForm, PicForm, DocFrom
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='/myapp/user/login/')
def user_profile(request):
    return render(request, 'myapp/profile/view.html')


@login_required(login_url='/myapp/user/login/')
def update_pic(request):
    template_data = parse_session(request, {'form_button': "Upload"})
    profile = request.user.account.profile
    request.POST._mutable = True
    if request.method == "POST":
        form = PicForm(request.POST, request.FILES)
        if form.is_valid():
            data = Profile.objects.get(pk=profile.pk)
            data.pic = form.cleaned_data['pic']
            data.save()
            form.assign(profile)
            profile.save()
            messages.success(request, 'Profile updated')
            return HttpResponseRedirect("/myapp/user/profile/")

    else:
        form = PicForm()
        template_data['form'] = form
    return render(request, 'myapp/profile/pic_form.html', template_data)


@login_required(login_url='/myapp/user/login/')
def update_view(request):
    template_data = parse_session(request, {'form_button': "Update profile"})
    # Proceed with the rest of the view
    profile = request.user.account.profile
    request.POST._mutable = True
    account = request.user.account
    request.POST['email'] = request.user.account.user.email
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            form.assign(profile)
            profile.save()
            messages.success(request, 'Profile updated')
            return HttpResponseRedirect("/myapp/user/profile/")
    else:
        form = ProfileForm(account.get_existed_data())
    form.disable_field('email')
    template_data['form'] = form
    return render(request, 'myapp/update.html', template_data)
