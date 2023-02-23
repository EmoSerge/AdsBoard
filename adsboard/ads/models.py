from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Advert(models.Model):
    TS = 'Tanks'
    HS = 'Healers'
    DD = 'Damage Dealers'
    TD = 'Traders'
    GM = 'Guild Masters'
    QG = 'Quest Givers'
    BS = 'Blacksmith'
    TN = 'Tanner'
    PM = 'Potion Master'
    SM = 'Spell Master'

    CATEGORY_TYPES = [
        (TS, 'Tanks'),
        (HS, 'Healers'),
        (DD, 'Damage Dealers'),
        (TD, 'Traders'),
        (GM, 'Guild Masters'),
        (QG, 'Quest Givers'),
        (BS, 'Blacksmith'),
        (TN, 'Tanner'),
        (PM, 'Potion Master'),
        (SM, 'Spell Master')
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=63)
    category = models.CharField(max_length=20, choices=CATEGORY_TYPES, default=TS)
    time_add = models.DateTimeField(auto_now_add=True)
    short_resp = models.CharField(max_length=255)
    content = RichTextUploadingField(config_name='default')

    def __str__(self):
        return f'Ad {self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('ad', args=[str(self.id)])


class Response(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Response author')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, verbose_name='Advert', related_name='response')
    time_resp = models.DateTimeField(auto_now_add=True)
    text_resp = models.TextField()
    status_delete = models.BooleanField(default=False, verbose_name='Response removed')
    status_accept = models.BooleanField(default=False, verbose_name='Response accepted')

    def __str__(self):
        return f'Response from {self.buyer} on ad {self.advert} '

    def get_absolute_url(self):
        return reverse('resp', args=[str(self.id)])
