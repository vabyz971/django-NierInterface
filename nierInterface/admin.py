# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T11:45:06-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-09-03T13:51:40-04:00
# @License: GPLv3
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin as DefaultSiteAdmin
from django.utils.translation import gettext_lazy as _

from .models import SiteConfig
from .forms import SiteConfigForm


class SiteConfigInline(admin.StackedInline):
    form = SiteConfigForm
    model = SiteConfig
    can_delete = False
    verbose_name_plural = _('site configuration')


class SiteAdmin(DefaultSiteAdmin):
    inlines = [SiteConfigInline]


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
