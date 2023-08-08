from django import forms

# internals
from .models import Developer, Skill


class DeveloperUpdateForm(forms.ModelForm):
    pass


class DeveloperForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    linkedin_pp_url = forms.URLField(widget=forms.TextInput, required=False)
    linkedin = forms.URLField(widget=forms.TextInput, required=False)
    twitter = forms.URLField(widget=forms.TextInput, required=False)
    github = forms.URLField(widget=forms.TextInput, required=False)
    website = forms.URLField(widget=forms.TextInput, required=False)

    class Meta:
        model = Developer
        fields = "__all__"
        exclude = ["user"]
