from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Account, Health, DocProfile


def validate_username_exist(username):
    if not User.objects.filter(username=username):
        raise forms.ValidationError('Username not existed')


def validate_phone_exist(phone):
    if  Profile.objects.filter(phone=phone).count():
        raise forms.ValidationError("The Phone number is registered")


def validate_email_available(email):
    if User.objects.filter(email=email).count():
        raise forms.ValidationError("The Email is already registered")


class BasicForm(forms.Form):
    def disable_field(self, field):
        self.fields[field].widget.attrs['disabled'] = ""

    def mark_error(self, field, description):
        self._errors[field] = self.error_class([description])
        del self.cleaned_data[field]


def setup_field(field, placeholder=None):
    field.widget.attrs['class'] = 'form_control'
    if placeholder is not None:
        field.widget.attrs['placeholder']=placeholder


class SignipUPform(BasicForm):
    username = forms.CharField(max_length=255,)
    setup_field(username, 'Enter Your username')
    email = forms.EmailField(max_length=50, validators=[validate_email_available], required=False)
    setup_field(email, 'Enter Your email ')
    phone = forms.CharField(max_length=11, min_length=11, required=False)
    setup_field(phone, ' Enter Phone number')
    password1 = forms.CharField(label='Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password1, 'Enter Your password')
    password2 = forms.CharField(label='', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password2, 'Enter Your password again')

    def clean(self):
        cleaned_data = super(SignipUPform, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.mark_error('password2', 'Passwords do not match')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        if email == "" and phone == "":
            self.mark_error('phone', 'Email or Phone one is required')
        return cleaned_data


class LoginForm(BasicForm):
    username = forms.CharField(max_length=50, validators=[validate_username_exist])
    setup_field(username, 'Enter Your username')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    setup_field(password, 'Enter Your password')

    def clean(self):
        """
        This is to make sure the password is valid for the given email. We don't have to worry about
        the email being invalid because the field specific validators run before this clean function.
        """
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.mark_error('password', 'Incorrect password')
        return cleaned_data


class PicForm(BasicForm):
    pic = forms.ImageField(label="", required=False)

    def assign(self, profile):
        profile.pic = self.cleaned_data['pic']


class ProfileForm(BasicForm):
    username = forms.CharField(max_length=255, required=False )
    setup_field(username, 'Enter Your username')
    email = forms.EmailField(max_length=50, required=False)
    setup_field(email, 'Enter Your email ')
    age = forms.CharField(max_length=255, required=False)
    setup_field(age, 'Enter Your age')
    phone = forms.CharField(max_length=255, required=False)
    setup_field(phone, 'Enter Your phone')
    sex = forms.ChoiceField(required=False, choices=Profile.SEX_TYPE )

    def assign(self, profile):
        profile.age = self.cleaned_data['age']
        profile.phone = self.cleaned_data['phone']
        profile.sex = self.cleaned_data['sex']


class AppointmentForm(BasicForm):
    patient = forms.ModelChoiceField(queryset=Account.objects.filter(role='PA'),)
    setup_field(patient)
    doctor = forms.ModelChoiceField(queryset=Account.objects.filter(role='DOC'),)
    setup_field(doctor)
    date = forms.DateField(input_formats=['%d-%m-%Y'])
    setup_field(date, 'D-M-Y')
    time = forms.TimeField()
    setup_field(time, ' H:M:S')

    def assign(self, appointment):
        """
        """
        appointment.doctor = self.cleaned_data['doctor'].user
        appointment.patient = self.cleaned_data['patient'].user
        appointment.date = self.cleaned_data['date']
        appointment.time = self.cleaned_data['time']


class PresForm(BasicForm):
    doctor = forms.ModelChoiceField(queryset=Account.objects.filter(role='DOC'),)
    patient = forms.ModelChoiceField(queryset=Account.objects.filter(role='PA'),)
    date = forms.DateField(input_formats=['%d-%m-%Y'])
    setup_field(date, 'D-M-Y')
    age = forms.CharField(max_length=200, required=False,)
    medications = forms.CharField(max_length=255, required=True,)


class MessageForm(BasicForm):
    sender = forms.ModelChoiceField(queryset=Account.objects.all(),)
    receiver = forms.ModelChoiceField(queryset=Account.objects.all(),)
    message = forms.CharField(max_length=255, required=False,)


class MsgForm(BasicForm):
    msg = forms.CharField(label="", max_length=1000, required=False,)


class MsgFileForm(BasicForm):
    msg = forms.FileField(label="", required=False)


class MsgPicForm(BasicForm):
    msg = forms.ImageField(label="", required=False)


class FileForm(BasicForm):
    msg = forms.FileField(label="", required=False)


class HealthForm(BasicForm):
    user = forms.ModelChoiceField(queryset=Account.objects.all())
    diabetic = forms.ChoiceField(required=False, choices=Health.HIGHNESS)
    setup_field(diabetic, '% of Your Diabetic')
    allergy = forms.ChoiceField(required=False, choices=Health.HIGHNESS)
    fiver = forms.ChoiceField(required=False, choices=Health.HIGHNESS)
    headache = forms.ChoiceField(required=False, choices=Health.HIGHNESS)
    setup_field(headache, '% of Your Headache')
    caff = forms.ChoiceField(required=False, choices=Health.HIGHNESS)
    body_pain = forms.ChoiceField(required=False, choices=Health.HIGHNESS)
    b_des = forms.CharField(max_length=200, required=False)
    setup_field(b_des, 'Describe here if any pain')
    comment = forms.CharField(max_length=200, required=False)

    def assign(self, health):
        health.user = self.cleaned_data['user'].user
        health.diabetic = self.cleaned_data['diabetic']
        health.allergy = self.cleaned_data['allergy']
        health.fiver = self.cleaned_data['fiver']
        health.caff = self.cleaned_data['caff']
        health.body_pain = self.cleaned_data['body_pain']
        health.b_des = self.cleaned_data['b_des']
        health.comment = self.cleaned_data['comment']


# for password

def validate_username(username):
    if not User.objects.filter(email=username).count():
        raise forms.ValidationError(" Email is not registered")


class PassChangeForm(BasicForm):
    password1 = forms.CharField(label='New', min_length=4, max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password again', min_length=4, max_length=50, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(PassChangeForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.mark_error('password2', 'Password  not matched')
        return cleaned_data


class PasswordForm(BasicForm):
    password = forms.CharField(label='', widget=forms.PasswordInput())
    setup_field(password, 'Your current password')


class EmailForm(BasicForm):
    email = forms.EmailField(label='', validators=[validate_username])
    setup_field(email, 'Your current email')


class ConfirmForm(BasicForm):
    code = forms.CharField(label='', max_length=6 )
    setup_field(code, 'Enter the code')


class DocFrom(BasicForm):
    user = forms.ModelChoiceField(queryset=Account.objects.all().filter(role='DOC'))
    specialist = forms.ChoiceField(choices=DocProfile.SPECIALIST, required=False)
    degree = forms.ChoiceField(choices=DocProfile.DEGREE, required=False)
    title = forms.CharField(required=False, max_length=200)
    description = forms.CharField(max_length=200, required=False)

    def assign(self, profile):
        profile.user=self.cleaned_data['user'].user
        profile.specialist=self.cleaned_data['specialist']
        profile.degree=self.cleaned_data['degree']
        profile.title=self.cleaned_data['title']
        profile.description=self.cleaned_data['description']