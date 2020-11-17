# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T11:45:06-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-11-17T08:19:43-04:00
# @License: GPLv3

from django.utils.translation import ugettext_lazy as _

from .generic import TemplateView, modal


class ElementTheme(TemplateView):
    title = _('Element theme')
    template_name = 'theme/element.html'


class ModalTheme(modal.TemplateView):

    title = _('Card Ajax')
    template_name = 'theme/modal.html'
