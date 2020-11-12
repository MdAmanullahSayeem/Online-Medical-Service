from django import template
from myapp.models import Appointment, Notification
from django.db.models import Q

register = template.Library()


@register.filter()
def msg(user):
    return Appointment.objects.filter(read=False, patient=user).count()


@register.filter()
def prescription(user):
    try:
        data = Notification.objects.get(user=user)
        var = data.prescription
        return var
    except:
        return None


@register.filter()
def message(user):
    try:
        data = Notification.objects.get(user=user)
        var = data.message
        return var
    except:
        return None


@register.filter()
def appointment(user):
    try:
        data = Appointment.objects.filter(patient=user, active='1').count()
        return data
    except:
        return None

@register.filter()
def friend(user1, user2):
    try:
        data=Appointment.objects.filter(Q(patient=user1 , doctor=user2) | Q(doctor=user1 , patient=user2))
        if data is not None:
            return True
        else:
            return False
    except:
        pass

