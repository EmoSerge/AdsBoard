from django import forms
from .models import Advert, Response


class AdForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = [
            'title',
            'category',
            'short_resp',
            'content',
        ]
        labels = {
            'title': 'Title',
            'category': 'Category',
            'short_resp': 'Short description',
            'content': 'Content'

        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text_resp',
        ]
        labels = {
            'text_resp': 'Response text',

        }


class ResponseAcceptForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = []
