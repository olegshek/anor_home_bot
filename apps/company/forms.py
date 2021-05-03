from django import forms


class ServiceForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'name_en',
            'name_ru',
            'name_uz',
            'description_en',
            'description_ru',
            'description_uz',
            'photo'
        )


class VacancyForm(forms.ModelForm):
    description_en = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_ru = forms.CharField(max_length=4000, widget=forms.Textarea)
    description_uz = forms.CharField(max_length=4000, widget=forms.Textarea)

    class Meta:
        fields = (
            'name_en',
            'name_ru',
            'name_uz',
            'description_en',
            'description_ru',
            'description_uz',
            'photo'
        )
