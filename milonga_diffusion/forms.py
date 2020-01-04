from django import forms
from crispy_forms.helper import FormHelper


class AddForm(forms.Form):
    # xsize = forms.CharField(label='x grid size', max_length=100)
    # ysize = forms.CharField(label='y grid size', max_length=100)
    x_size = forms.IntegerField( 
    label = "",
    validators = [lambda x: x<30],
    widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    y_size = forms.IntegerField(
    label = "",
    widget=forms.TextInput(
    attrs={'class': 'form-control',}
    ))


