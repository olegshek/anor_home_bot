from django import forms


class TextForm(forms.ModelForm):
    text_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    text_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    text_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'text_en',
            'text_ru',
            'text_uz'
        )
