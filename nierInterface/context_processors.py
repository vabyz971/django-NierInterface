# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T11:51:33-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-09-03T11:53:52-04:00
# @License: GPLv3

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sites.models import Site


def template_var(context):
    """ Renvoir les parametres du site pour NierInterface """
    return {
        'CURRENT_SITE': Site.objects.get_current(),
    }
