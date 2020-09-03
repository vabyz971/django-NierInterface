# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T11:45:06-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-09-03T13:50:07-04:00
# @License: GPLv3

from __future__ import unicode_literals
import os

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site


class SiteConfig(models.Model):
    """Configurations complémentaires pour un site web"""
    site = models.OneToOneField(Site,
                                on_delete=models.PROTECT,
                                verbose_name=_('site'),
                                related_name='config')
    file_upload = models.ImageField(_('logo'),
                                    upload_to='nier_logos',
                                    blank=True,
                                    null=True)
    favicon = models.FileField(_('favicon'),
                               upload_to='nier_favicons',
                               blank=True,
                               null=True)
    slogan = models.CharField(_('slogan'), max_length=100, blank=True)
    short_description = models.CharField(_('short descripion'),
                                         max_length=500,
                                         blank=True)
    keywords = models.CharField(_('keywords'),
                                max_length=100,
                                blank=True,
                                help_text=_('separate words with comma'))

    def __str__(self):
        return self.site.name

    @property
    def logo(self):
        """Champs logo pour surcharger file_upload"""
        return self.file_upload

    def remove_file(self, field_name=None):
        """Supprime physiquement le fichier

        Args:
            field_name: None du champs où est stocké le fichier

        Returns:
            Oui ou non si la suppression a réussi ou non
        """
        field = getattr(self, field_name, False)
        if field:
            if os.path.exists(field.path):
                os.remove(field.path)
                return True
        return False

    def save(self, *args, **kwargs):
        """Vérifie si le fichier a été supprimé ou changé pour savoir
        si on supprime physiquement
        """
        if self.pk:
            doc = self.__class__.objects.get(pk=self.pk)
            if not self.file_upload == doc.file_upload:
                doc.remove_file('file_upload')
            if not self.favicon == doc.favicon:
                doc.remove_file('favicon')

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('site configuration')
        verbose_name_plural = _('sites configurations')
        ordering = ('site', )


def remove_file(sender, instance=None, **kwargs):
    """ Supprime le fichier après la suppression de l'objet.
    À utiliser avec un post_delete
    """
    if instance is None:
        return
    instance.remove_file('file_upload')
    instance.remove_file('favicon')


post_delete.connect(remove_file, sender=SiteConfig)


def setup_config(sender, instance, created, **kwargs):
    """Assure que tous les sites ont une config"""
    config = SiteConfig.objects.get_or_create(site=instance, defaults={})


post_save.connect(setup_config, sender=Site)
