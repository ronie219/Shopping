from django import forms

from .models import Item

class itemAddingForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            'category',
            'name',
            'prize',
            'description',
            'count'
        ]

    def validate(self,data):
        desc = data.cleaned_data['description']
        print(desc)
        if len(desc) < 15:
            raise forms.ValidationError("Desc is Short")
        return data