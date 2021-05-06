from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ProjectForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'name',
            'description_en',
            'description_ru',
            'description_uz',
            'main_photo',
            'photos',
            'documents',
            'location',
            'catalogue_documents'
        )


class LocationForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'description_en',
            'description_ru',
            'description_uz',
            'address'
        )


class ApartmentForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'project',
            'duplex',
            'room_quantity',
            'square',
            'floor_number',
            'description_en',
            'description_ru',
            'description_uz',
            'photos'
        )

    def clean(self):
        data = self.cleaned_data

        if data.get('duplex', None):
            if not data.get('floor_number', None):
                raise ValidationError(_('Floor number is required for duplex'))

            if data['floor_number'] in data['duplex'].apartments.exclude(
                    id=self.instance.id if self.instance else None
            ).values_list('floor_number', flat=True):
                raise ValidationError(_('Apartment with such floor number is already exist'))

        if not data.get('duplex', None) and (not data.get('project', None) or not data.get('room_quantity', None)):
            raise ValidationError(_('Project and room_quantity are required for not duplex apartment'))

        return super().clean()


class StoreForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'project',
            'square',
            'floor_number',
            'description_en',
            'description_ru',
            'description_uz',
            'photos'
        )
