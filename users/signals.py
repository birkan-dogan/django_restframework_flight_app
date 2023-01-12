from django.contrib.auth.models import User
from django.db.models.signals import post_save  # user create edilince signal'i gönderecek method

from django.dispatch import receiver  # signal'i yakalayacak decorator

from rest_framework.authtoken.models import Token  # signal yakalndıktan sonra token'ımızı create edeceğimiz Token database_table'ı


@receiver(post_save, sender = User)
def create_Token(sender, instance = None, created = False, **kwargs):
    if(created):
        Token.objects.create(user = instance)
