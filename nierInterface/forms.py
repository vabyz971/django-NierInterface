# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T14:03:09-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-09-03T14:03:31-04:00
# @License: GPLv3

from __future__ import unicode_literals

from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site

from crispy_forms.helper import FormHelper

from .models import SiteConfig


class SiteConfigForm(forms.ModelForm):
    """Formulaire d'edition de la configuration de site"""
    ALLOWED_CONTENT_TYPES = ['png', 'vnd.microsoft.icon']

    def __init__(self, *args, **kwargs):
        super(SiteConfigForm, self).__init__(*args, **kwargs)
        self.fields['favicon'].help_text = _(
            "The file must be a valid icon format: .ico or .png")

    def clean_favicon(self):
        favicon = self.cleaned_data.get('favicon')
        if favicon:
            try:
                content_type = favicon.content_type.split('/')[1]
                if content_type not in self.ALLOWED_CONTENT_TYPES:
                    raise forms.ValidationError(
                        _('Upload a valid file. The file you uploaded was '
                          'either not a valid file type or a corrupted '
                          'image.'))
            except AttributeError:
                pass
        return favicon

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        return helper

    class Meta:
        model = SiteConfig
        fields = '__all__'
        widgets = {
            'short_description': forms.Textarea,
        }


SiteConfigFormset = forms.inlineformset_factory(Site,
                                                SiteConfig,
                                                form=SiteConfigForm,
                                                max_num=1,
                                                can_delete=False)


class CurrentSiteForm(forms.ModelForm):
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        return helper

    class Meta:
        model = Site
        fields = '__all__'
