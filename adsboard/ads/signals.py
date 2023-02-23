from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from ads.models import Advert, Response
from adsboard.settings import SITE_URL, DEFAULT_FROM_EMAIL


def send_note_new_advert(title, short_resp, pk, us_emails):
    html_content = render_to_string(
        'ad_created_email.html',
        {
            'title': title,
            'text': short_resp,
            'link': f'{SITE_URL}/adsboard/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=us_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Advert)
def notify_about_new_ads(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        us_emails = []
        us_emails += [u.email for u in users]
        send_note_new_advert(instance.title, instance.short_resp, instance.pk, us_emails)


def send_note_new_resp(text_resp, pk, buyer, us_emails, advert):
    html_content = render_to_string(
        'resp_created_email.html',
        {
            'title': 'New response',
            'text': text_resp,
            'link': f'{SITE_URL}/adsboard/responses/{pk}',
            'buyer': buyer,
            'advert': f'{SITE_URL}/adsboard/{advert.id}'
        }

    )

    msg = EmailMultiAlternatives(
        subject='New response',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=us_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Response)
def notify_about_new_resp(sender, instance, created, **kwargs):
    if created:
        us_emails = [User.objects.get(id=instance.advert.author.id).email]
        send_note_new_resp(instance.text_resp, instance.pk, instance.buyer, us_emails, instance.advert)


def send_note_del_resp(pk, buyer, us_emails, advert):
    html_content = render_to_string(
        'resp_deleted_email.html',
        {
            'link': f'{SITE_URL}/adsboard/response/{pk}',
            'buyer': buyer,
            'advert': f'{SITE_URL}/adsboard/{advert.id}'
        }

    )

    msg = EmailMultiAlternatives(
        subject='Your response has been deleted',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=us_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Response)
def notify_about_new_ads(sender, instance, **kwargs):
    if instance.status_delete:
        us_emails = [User.objects.get(id=instance.buyer.id).email]
        send_note_del_resp(instance.pk, instance.buyer, us_emails, instance.advert)


def send_note_accept_resp(pk, buyer, us_emails, advert):
    html_content = render_to_string(
        'resp_accepted_email.html',
        {
            'link': f'{SITE_URL}/adsboard/response/{pk}',
            'buyer': buyer,
            'advert': f'{SITE_URL}/adsboard/{advert.id}'
        }

    )

    msg = EmailMultiAlternatives(
        subject='Your response has been accepted',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=us_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Response)
def notify_about_new_ads(sender, instance, **kwargs):
    if instance.status_accept:
        us_emails = [User.objects.get(id=instance.buyer.id).email]
        send_note_accept_resp(instance.pk, instance.buyer, us_emails, instance.advert)
