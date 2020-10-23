# -*- coding: utf-8 -*-
#
# This file is part of Bootstrap for Django
#
# Bootstrap for Django is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Bootstrap for Django is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Bootstrap for Django.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2016 IPEOS I-Solutions
# par Laurent Vergerolle <laurent@ipeos.com>
#
# Class based view spécifiques pour les modals
#
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db.models import ProtectedError

from nierInterface import generic


class FormMixin(generic.FormMixin):
    """Transforme la fonction form_valid pour un retour dans une modal

    Attributes:
        refresh_page: Permet de recharger la page globale accueillant la modal
        refresh_modal: Permet de charger le résultat directement dans
            la fenètre de la modal même si ce n'est pas une popup
    """
    template_name = 'form-modal.html'
    template_success_name = 'form-modal-success.html'
    success_message = _('saved successfully')
    save_data_message = _('Save data')
    save_data_text = _('Save current data.')
    refresh_page = True
    refresh_modal = False
    refresh_new_page = False
    close_button = False
    modal_size = None

    def get_save_data_message(self):
        return self.save_data_message

    def get_save_data_text(self):
        return self.save_data_text

    def get_close_button(self):
        return self.close_button

    def get_modal_size(self):
        return self.modal_size

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['close_button'] = self.get_close_button()
        ctx['modal_size'] = self.get_modal_size()
        return ctx

    def form_valid(self, form, commit=True):
        """Lors de la validation, commit donne la possibilité à l'héritier
        de stopper la sauvegarde pour surcharger le modèle comme la méthode
        `save` des Forms (pouvoir rajouter des valeurs à l'instance
        sauvegardée avant l'enregistrement final).

        Args:
            form: formulaire a traiter
            commit: flag permettant d'activer ou pas la sauvegarde
                directe du formulaire.

        Returns:
            En fonction de commit :
                - Si commit est vrai alors on renvoie la requète HTTP pour
                    la modal.
                - Si commit est faux alors on renvoie un tuple contenant
                    l'instance en attente de sauvegarde et la requète HTTP
                    que l'héritier devra servir à la modal à la fin du
                    traitement.
        """
        messages.success(self.request, self.get_success_message())

        ctx = {
            'title': self.get_save_data_message(),
            'content_text': self.get_save_data_text(),
            'refresh_page': self.refresh_page,
            'refresh_modal': self.refresh_modal,
            'refresh_new_page': self.refresh_new_page
        }

        if self.refresh_modal and self.refresh_page:
            self.request.session['refresh_needed'] = True

        try:
            ctx['success_url'] = self.get_success_url()
        except ImproperlyConfigured:
            ctx['success_url'] = None

        # Informations en cas de popup
        if self.request.GET.get('popup'):
            ctx['popup'] = 1

        if commit:
            return HttpResponse(
                render_to_string(self.template_success_name, ctx))

        return (None,
                HttpResponse(render_to_string(self.template_success_name,
                                              ctx)))


class ModelFormMixin(FormMixin, generic.ModelFormMixin):
    def form_valid(self, form, commit=True):
        self.object = form.save(commit)
        ret = super().form_valid(form, False)

        if commit:
            return ret[1]

        return (self.object, ret[1])


class DeletionMixin(generic.DeletionMixin):
    """Transforme la fonction delete pour un retour dans une modal

    Attributes:
        refresh_page: Permet de recharger la page globale accueillant la modal
        refresh_modal: Permet de charger le résultat directement dans
            la fenètre de la modal même si ce n'est pas une popup
    """
    template_name = 'delete-modal.html'
    save_data_message = _('Delete data')
    save_data_text = _('Delete current data.')
    refresh_page = True
    refresh_modal = False
    refresh_new_page = False
    modal_size = None

    def get_save_data_message(self):
        return self.save_data_message

    def get_save_data_text(self):
        return self.save_data_text

    def get_modal_size(self):
        return self.modal_size

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['modal_size'] = self.get_modal_size()
        return ctx

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()

            messages.warning(self.request,
                             self.get_delete_message(self.object))
        except ProtectedError:
            messages.error(self.request,
                           self.get_object_protect_message(self.object))

        ctx = {
            'title': self.get_save_data_message(),
            'content_text': self.get_save_data_text(),
            'refresh_page': self.refresh_page,
            'refresh_modal': self.refresh_modal,
            'refresh_new_page': self.refresh_new_page
        }

        if self.refresh_modal and self.refresh_page:
            self.request.session['refresh_needed'] = True

        try:
            ctx['success_url'] = self.get_success_url()
        except ImproperlyConfigured:
            ctx['success_url'] = None

        return HttpResponse(render_to_string('form-modal-success.html', ctx))


class TemplateView(generic.TemplateView):
    """TemplateView pour les modals"""
    extend_template = 'base-modal.html'
    refresh_page = None
    modal_size = None

    def get_refresh_page(self):
        if self.refresh_page is None:
            refresh = self.request.session.get('refresh_needed', False)
            self.request.session['refresh_needed'] = False
            return refresh
        return self.refresh_page

    def get_modal_size(self):
        return self.modal_size

    def get_context_data(self, **kwargs):
        ctx = super(TemplateView, self).get_context_data(**kwargs)
        ctx['refresh_page'] = self.get_refresh_page()
        ctx['modal_size'] = self.get_modal_size()
        return ctx


class DetailView(generic.DetailView):
    """DetailView pour les modals"""
    extend_template = 'base-modal.html'
    template_name = 'base-modal.html'
    refresh_page = None
    modal_size = None

    def get_refresh_page(self):
        if self.refresh_page is None:
            refresh = self.request.session.get('refresh_needed', False)
            self.request.session['refresh_needed'] = False
            return refresh
        return self.refresh_page

    def get_modal_size(self):
        return self.modal_size

    def get_context_data(self, **kwargs):
        ctx = super(DetailView, self).get_context_data(**kwargs)
        ctx['refresh_page'] = self.get_refresh_page()
        ctx['modal_size'] = self.get_modal_size()
        return ctx


class FormView(FormMixin, generic.FormView):
    """FormView pour les modals"""


class ListView(generic.ListView):
    """ListView pour les modals"""
    extend_template = 'base-modal.html'
    template_name = 'base-modal.html'
    refresh_page = None
    modal_size = None

    def get_refresh_page(self):
        if self.refresh_page is None:
            refresh = self.request.session.get('refresh_needed', False)
            self.request.session['refresh_needed'] = False
            return refresh
        return self.refresh_page

    def get_modal_size(self):
        return self.modal_size

    def get_context_data(self, **kwargs):
        ctx = super(ListView, self).get_context_data(**kwargs)
        ctx['refresh_page'] = self.get_refresh_page()
        ctx['modal_size'] = self.get_modal_size()
        return ctx


class CreateView(ModelFormMixin, generic.CreateView):
    """CreateView pour les modals"""


class UpdateView(ModelFormMixin, generic.UpdateView):
    """UpdateView pour les modals"""


class DeleteView(DeletionMixin, generic.DeleteView):
    """DeleteView pour les modals"""
