from django import forms


class PhotoForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'description_en',
            'description_ru',
            'description_uz',
            'photo'
        )


class DocumentForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'description_en',
            'description_ru',
            'description_uz',
            'document'
        )


