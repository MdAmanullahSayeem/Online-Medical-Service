from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# Create your models here.


class Profile(models.Model):
    SEX_TYPE = (
        ('M', 'male'),
        ('F', 'female'),
        ('O', 'other'),
    )
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(blank=True, max_length=255,)
    sex = models.CharField(blank=True, max_length=1, choices=SEX_TYPE,)
    phone = models.CharField(blank=True, max_length=255,)
    pic = models.ImageField(blank=True, null=True, upload_to='Profile/picture/')


    """""
    To get existing datra to the fields
    """""

    def get_existed_data(self):
        fields = {}
        if self.age is not None:
            fields['age'] = self.age
        if self.phone is not None:
            fields['phone'] = self.phone
        if self.sex is not None:
            fields['sex'] = self.sex
        if self.pic is not None:
            fields['pic'] = self.pic
        return fields

    def __str__(self):
        return self.user.username


class Account(models.Model):
    ADMIN = 'AD'
    PATIENT = 'PA'
    DOCTOR = 'DOC'
    EMPLOYEE = 'EMP'
    OTHER = 'OT'
    ACCOUNT_TYPES = [
        (ADMIN, 'Admin'),
        (PATIENT, 'patient'),
        (DOCTOR, 'doctor'),
        (EMPLOYEE, 'employee'),
        (OTHER, 'other'),
    ]

    role = models.CharField(max_length=3, choices=ACCOUNT_TYPES, default=PATIENT,)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,)
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    def get_existed_data(self):
        fields = {}

        if self.user.username is not None:
            fields['username'] = self.user.username
        if self.user.email is not None:
            fields['email'] = self.user.email
        if self.role is not None:
            fields['role'] = self.role
        if self.profile.age is not None:
            fields['age'] = self.profile.age
        if self.profile.phone is not None:
            fields['phone'] = self.profile.phone
        if self.profile.sex is not None:
            fields['sex'] = self.profile.sex
        return fields

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    description = models.CharField(max_length=255, blank=True,)
    date = models.DateField()
    time = models.TimeField(default=timezone.now())
    active = models.BooleanField(default=False, null=True, blank=True,)
    read = models.BooleanField(default=False,)

    def get_existed_data(self):
        fields = {
            'doctor': self.doctor.account,
            'patient': self.patient.account,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'active': self.active,
        }
        return fields


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    date = models.DateField()
    age = models.CharField(max_length=200, null=True)
    medications = models.CharField(max_length=255)
    read = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=255, blank=True,)
    file = models.FileField(null=True, blank=True, upload_to='Message/file/')
    pic = models.ImageField(null=True, blank=True, upload_to='Message/pic/')
    read = models.BooleanField(default=False,)
    timestamp = models.DateTimeField(auto_now_add=True,)


class Health(models.Model):
    HIGHNESS = [
        ('No', 'No'),
        ('20%', '20%'),
        ('40%', '40%'),
        ('60%', '60%'),
        ('80%', '80%'),
        ('90%', '90%'),
        ('100%', '100%'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    T_report = models.FileField(blank=True, null=True, upload_to='profile/health/document/')
    diabetic = models.CharField(max_length=20, default='No', choices=HIGHNESS, null=True, blank=True)
    allergy = models.CharField(max_length=20, default='No', choices=HIGHNESS, null=True, blank=True)
    fiver = models.CharField(max_length=20, default='No', choices=HIGHNESS, null=True, blank=True)
    headache = models.CharField(max_length=20, default='No', choices=HIGHNESS, null=True, blank=True)
    caff = models.CharField(max_length=20, default='No', choices=HIGHNESS, null=True, blank=True)
    body_pain = models.CharField(max_length=20, default='No', choices=HIGHNESS, null=True, blank=True)
    b_des = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def get_existed_data(self):
        fields = {
            'user': self.user.account,
            'T_report': self.T_report,
            'diabetic': self.diabetic,
            'allergy': self.allergy,
            'fiver': self.fiver,
            'headache': self.headache,
            'caff': self.caff,
            'body_pain': self.body_pain,
            'b_des ': self.b_des,
            'comment': self.comment,
        }
        return fields

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    appointment = models.IntegerField(null=True, blank=True)
    prescription = models.IntegerField(null=True, blank=True)
    message = models.IntegerField(null=True, blank=True)


class Password(models.Model):
    email = models.CharField(max_length=200,)
    code = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)

    @property
    def validate_code(self):
        if timezone.now().minute - self.timestamp.minute > 1:
            self.delete()
            return True
        else:
            return False


class DocProfile(models.Model):
    SPECIALIST = [
        ('Eye/Year/Throat ', 'Eye/Year/Throat '),
        ('Dental', 'Dental'),
        ('Child ', 'child'),
        ('gynecologist ', 'gynecologist'),
        ('Dermatologists', 'Dermatologists'),
        ('Plastic Surgeons', 'Plastic Surgeons'),
        ('Psychiatrists', 'Psychiatrists'),
        ('General Surgeons', 'General Surgeons'),
        ('Urologists', 'Urologists'),
        ('Pathologists', 'Pathologists'),
    ]
    DEGREE = [
        ('MBBS', 'MBBS'),
        ('FCPS', 'FCPS'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    specialist = models.CharField(max_length=20, choices=SPECIALIST, null=True)
    degree = models.CharField(max_length=20, choices=DEGREE, null=True)
    title = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def get_existed_data(self):
        fields = {
            'user': self.user.account,
            'specialist': self.specialist,
            'degree': self.degree,
            'title': self.title,
            'description': self.description,
        }
        return fields
