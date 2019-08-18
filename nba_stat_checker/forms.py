from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(strip=True,max_length=26,widget=forms.TextInput(attrs={
        'class':'form-control rounded-0',
        'placeholder':'Search'
    }),label='')
    