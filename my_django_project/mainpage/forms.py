from django import forms

from .models import KrasLocation, SfuLocation


class LocationTypeForm(forms.Form):
    location_type = forms.ChoiceField(
        choices=(
            ('sfu', 'SFU'),
            ('kras', 'Kras'),
        ),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Тип локации',
    )


class BaseLocationForm(forms.ModelForm):
    photo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        })
    )
    latitude = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': 'any',
            'placeholder': '55.996973',
        })
    )
    longitude = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': 'any',
            'placeholder': '92.795429',
        })
    )

    class Meta:
        fields = ['photo', 'latitude', 'longitude']


class SfuLocationForm(BaseLocationForm):
    class Meta(BaseLocationForm.Meta):
        model = SfuLocation


class KrasLocationForm(BaseLocationForm):
    class Meta(BaseLocationForm.Meta):
        model = KrasLocation