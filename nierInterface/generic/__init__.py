# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T10:25:28-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-10-22T22:32:15-04:00
# @License: GPLv3
#
# Surcharge des classes based views
#

from __future__ import unicode_literals

from django.views.generic.base import TemplateResponseMixin\
    as DefaultTemplateResponseMixin
from django.views.generic.base import ContextMixin as DefaultContextMixin
from django.views.generic.edit import FormMixin as DefaultFormMixin
from django.views.generic.edit import ModelFormMixin as DefaultModelFormMixin
from django.views.generic.edit import DeletionMixin as DefaultDeletionMixin
from django.views.generic import TemplateView as DefaultTemplateView
from django.views.generic import ListView as DefaultListView
from django.views.generic import FormView as DefaultFormView
from django.views.generic import CreateView as DefaultCreateView
from django.views.generic import UpdateView as DefaultUpdateView
from django.views.generic import DeleteView as DefaultDeleteView
from django.views.generic import DetailView as DefaultDetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect

from crispy_forms.helper import FormHelper


class FormMixin(DefaultFormMixin):
    """Supprime les tags <form></form>  par défaut pour les formulaires
    qui n'ont pas de helper et ajoute automatiquement un message
    d'erreur pour les formulaires dans le cas d'echec de traitement.
    """
    all_form_button = True
    submit_name = _('Save')
    submit_btn_class = 'btn'
    success_message = _('Your input has been saved.')
    error_message = _('Please correct the errors below.')
    cancel_url = None
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_success_message(self):
        return self.success_message

    def get_success_url(self):
        success_url = super().get_success_url()
        redirect_url = self.request.POST.get(self.redirect_field_name)
        if redirect_url:
            return str(redirect_url)
        return success_url

    def get_error_message(self):
        return self.error_message

    def get_cancel_url(self):
        return self.cancel_url

    def get_all_form_button(self):
        return self.all_form_button

    def get_submit_name(self):
        return self.submit_name

    def get_submit_btn_class(self):
        return self.submit_btn_class

    def get_form(self, form_class=None):
        form = super(FormMixin, self).get_form(form_class)
        # Ajoute les attributs helper par défaut aux formulaires
        try:
            form.helper
        except AttributeError:
            form.helper = FormHelper()
            form.helper.form_tag = False
            form.helper.include_media = False
        return form

    def form_valid(self, form):
        try:
            self.object = form.save()
        except AttributeError:
            pass
        messages.success(self.request, self.get_success_message())
        return super(FormMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.get_error_message())
        return super(FormMixin, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super(FormMixin, self).get_context_data(**kwargs)
        ctx['submit_name'] = self.get_submit_name()
        ctx['cancel_url'] = self.get_cancel_url()
        ctx['all_form_button'] = self.get_all_form_button()
        ctx['submit_btn_class'] = self.get_submit_btn_class()
        ctx['redirect_field_name'] = self.redirect_field_name
        ctx['redirect_field_value'] = self.request.GET.get(
            self.redirect_field_name)
        return ctx


class ModelFormMixin(FormMixin, DefaultModelFormMixin):
    def form_valid(self, form):
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)


class DeletionMixin(DefaultDeletionMixin):
    """Ajoute les actions par défaut faites par les vues de suppression
    """
    template_name = 'delete.html'
    title = _('Are you sure?')
    delete_message = _('Successfully deleted data.')
    context_object_name = 'item'
    cancel_url = None

    def get_cancel_url(self):
        return self.cancel_url

    def get_delete_message(self, object_name=None):
        """Message de réussite de suppression des données a afficher
        après la fermeture de la fenetre modal

        :param object_name: objet supprimé utile pour la construction
            du message de retour
        :return: message a afficher dans la fenètre de succès
        :rtype: unicode or translation
        """
        return self.delete_message

    def get_object_protect_message(self, object_name):
        """Message d'erreur dans le cas où un objet est protégé dans la
        base et ne peut pas être supprimé.

        :param object_name: objet a supprimé utilise pour la construction
            du message de retour
        :return: message a afficher dans la fenètre d'erreur
        :rtype: unicode or translation
        """
        return _('<b>An error occurred:</b><br/>'
                 'The record <i>"{0}"</i> can not be deleted. '
                 'This data is already used by a main object in '
                 'data base.').format(object_name)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            messages.warning(self.request,
                             self.get_delete_message(self.object))
            return super(DeletionMixin, self).delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request,
                           self.get_object_protect_message(self.object))
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        ctx = super(DeletionMixin, self).get_context_data(**kwargs)
        ctx['cancel_url'] = self.get_cancel_url()
        return ctx.copy()


class TemplateResponseFormMixin(DefaultTemplateResponseMixin):
    def get_template_names(self):
        """Ajout la vue form.html comme vu par défaut"""
        try:
            template_names = super(TemplateResponseFormMixin,
                                   self).get_template_names()
            return template_names + ['form.html']
        except ImproperlyConfigured:
            return ['form.html']


class ContextMixin(DefaultContextMixin):
    """Ajoute des attributs aux classes de bases

    :param title: Titre de la page
    :param submit_name: Nom du bouton submit (pour les formulaires)
    :param cancel_url: url de redirection en cas d'annulation
        (pour les formulaires)
    :param extend_template: Template d'où la page est étendue
    :param content_text: Texte pouvant être affiché dans le template
        depuis la vue. Par défaut ce paramètre est vide. Ce contenu
        peut être multiligne mais ne peut contenir de balise HTML.
    """
    title = ""
    extend_template = 'site_base.html'
    content_text = None
    content_text_class = None

    def get_title(self):
        return self.title

    def get_content_text(self):
        return self.content_text

    def get_content_text_class(self):
        return self.content_text_class

    def get_extend_template(self):
        return self.extend_template

    def get_context_data(self, **kwargs):
        ctx = super(ContextMixin, self).get_context_data(**kwargs)
        ctx['title'] = self.get_title()
        ctx['extend_template'] = self.get_extend_template()
        ctx['content_text'] = self.get_content_text()
        ctx['content_text_class'] = self.get_content_text_class()
        try:
            # Ajoute le model au si il existe pour l'utilisation de constante
            ctx['model'] = self.model
        except AttributeError:
            pass
        return ctx.copy()


class TemplateView(ContextMixin, DefaultTemplateView):
    """TemplateView étendue"""


class ListView(ContextMixin, DefaultListView):
    """ListView étendue"""
    paginate_by = 20
    context_object_name = 'items'
    fields = None
    add_in_modal = True
    edit_in_modal = True
    delete_in_modal = True
    add_url = None
    edit_url_name = None
    delete_url_name = None
    detail_url_name = None
    btn_add_title = _('Add')

    def get_fields(self):
        if self.fields is None:
            return ()
        return self.fields

    # def get_queryset(self):
    #     """Inclus le tri pour les listes de données.
    #
    #     Il suffit d'ajouter un lien ?order_by=parametre pour trier
    #     en fonction de ce paramètre.
    #     """
    #     queryset = super(ListView, self).get_queryset()
    #
    #     if self.get_display_search():
    #         return self.search_queryset(queryset)
    #     return queryset

    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        names.append('list.html')
        return names

    def get_add_in_modal(self):
        return self.add_in_modal

    def get_edit_in_modal(self):
        return self.edit_in_modal

    def get_delete_in_modal(self):
        return self.delete_in_modal

    def get_add_url(self):
        return self.add_url

    def get_edit_url_name(self):
        # Permet de retrouver l'url à partir du nom + pk
        return self.edit_url_name

    def get_delete_url_name(self):
        # Permet de retrouver l'url à partir du nom + pk
        return self.delete_url_name

    def get_detail_url_name(self):
        # Permet de retrouver l'url à partir du nom + pk
        return self.detail_url_name

    def get_context_data(self, **kwargs):
        ctx = super(ListView, self).get_context_data(**kwargs)
        ctx['fields'] = self.get_fields()
        ctx['add_in_modal'] = self.get_add_in_modal()
        ctx['edit_in_modal'] = self.get_edit_in_modal()
        ctx['delete_in_modal'] = self.get_delete_in_modal()
        ctx['add_url'] = self.get_add_url()
        ctx['edit_url_name'] = self.get_edit_url_name()
        ctx['delete_url_name'] = self.get_delete_url_name()
        ctx['detail_url_name'] = self.get_detail_url_name()
        return ctx


class FormView(FormMixin, TemplateResponseFormMixin, ContextMixin,
               DefaultFormView):
    """FormView étendue"""


class CreateView(ModelFormMixin, TemplateResponseFormMixin, ContextMixin,
                 DefaultCreateView):
    """CreateView étendue"""


class UpdateView(ModelFormMixin, TemplateResponseFormMixin, ContextMixin,
                 DefaultUpdateView):
    """UpdateView étendue"""


class DeleteView(DeletionMixin, ContextMixin, DefaultDeleteView):
    """DeleteView étendue"""


class DetailView(ContextMixin, DefaultDetailView):
    """DetailView étendue"""
