# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T11:36:27-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-09-03T11:43:48-04:00
# @License: GPLv3

from __future__ import unicode_literals
from django.apps import AppConfig as DefaultAppConfig


class AppConfig(DefaultAppConfig):
    name = 'nierInterface'
    verbose_name = 'NierAutomata Interface'

    def ready(self):
        if 'sass_processor.finders.CssFinder' not in \
                settings.STATICFILES_FINDERS:
            settings.STATICFILES_FINDERS.append(
                'sass_processor.finders.CssFinder')
