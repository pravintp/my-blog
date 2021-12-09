from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    share_text = forms.CharField(required=False, widget=forms.Textarea)
