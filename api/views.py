from django.shortcuts import render
from django.core.mail import send_mail
from api_yamdb import settings
import random


def get_email_code(email):
    chars = (
        'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNO'
        'PQRSTUVWXYZ1234567890'
    )
    for n in range(1):
        password = ''
        for i in range(18):
            password += random.choice(chars)
        send_mail(
            'Password',
            password,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )
