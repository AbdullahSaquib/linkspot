from django import forms

class AddCategoryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    summary = forms.CharField(label='Summary', widget=forms.Textarea ,max_length=500)

class AddPageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    summary = forms.CharField(label='Summary', widget=forms.Textarea ,max_length=500)
    url = forms.URLField(label='URL', max_length=100)

class AddCommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs = {
            'id':'new-comment',
            'placeholder':'Post your thoughts'
            }
    ))
