from django.shortcuts import render
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message, Appointment, Prescription, Health, Account, Profile, Notification, DocProfile
from django.contrib.auth.models import User
import datetime


@receiver(post_save, sender=Appointment)
def notify_apo(sender, instance, created, **kwargs):
    patient = instance.patient
    doctor = instance.doctor
    number1 = Appointment.objects.filter(patient=patient,read=False).count()
    number2 = Appointment.objects.filter(doctor=doctor,read=False).count()
    data1 = Notification.objects.filter(user=patient).count()
    data2 = Notification.objects.filter(user=doctor).count()
    if data1 == 0:
        Notification.objects.create(user=patient, appointment=number1)
    else:
        Notification.objects.filter(user=patient).update(appointment=number1)
    if data2 == 0:
        Notification.objects.create(user=doctor, appointment=number2)
    else:
        Notification.objects.filter(user=doctor).update(appointment=number2)


@receiver(post_save, sender=Message)
def notify_msg(sender, instance, created, **kwargs):
    #create or update both notify msg receiver
    number = Message.objects.filter(receiver=instance.receiver, read=False).count()
    data = Notification.objects.filter(user=instance.receiver).count()
    print('dada',data)
    if data == 0:
        Notification.objects.create(user=instance.receiver, message=number)
        print('create',instance.receiver)
    else:
        Notification.objects.filter(user=instance.receiver).update(message=number)
        print('update',instance.receiver)


@receiver(post_save, sender=Prescription)
def notify_pres(sender, instance, created, **kwargs):
    user = instance.patient
    number = Prescription.objects.filter(read=False).count()
    data = Notification.objects.filter(user=user).count()
    if data == 0:
        Notification.objects.create(user=user, prescription=number)
    else:
        Notification.objects.filter(user=user).update(prescription=number)




@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("profile created")

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        instance.profile.save()
        print("profile updated")

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(
            user=instance,
            profile=instance.profile
        )
        print("account created")

@receiver(post_save, sender=User)
def update_account(sender, instance, created, **kwargs):
    if not created:
        instance.account.save()
        print("account updated")
