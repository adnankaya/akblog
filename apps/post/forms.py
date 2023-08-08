# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput

# internals
from .models import Post, PostImage


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = _('Title')
        self.fields['body'].label = _('Description')
        self.fields['category'].label = _('Category')

    class Meta:
        model = Post
        fields = ('title', 'body', "category")


class PostUpdateForm(PostForm):
    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        self.fields['tags'].label = _('Tags')

    class Meta(PostForm.Meta):
        fields = PostForm.Meta.fields + ('tags', )


    def clean_tags(self):
        tags = self.cleaned_data.get('tags', [])
        if (len(tags) < 2 or len(tags) > 5):
            raise ValidationError(
                _("Tags must be min 2 and max 5"), code='invalid')
        return tags


class PostSearchForm(forms.Form):
    query = forms.CharField()


class PostImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = PostImage
        fields = ("image", )
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }
