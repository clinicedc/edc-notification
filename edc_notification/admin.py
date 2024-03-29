from django.contrib import admin
from django.contrib.admin.decorators import register
from edc_model_admin.mixins import TemplatesModelAdminMixin

from .admin_site import edc_notification_admin
from .models import Notification


@register(Notification, site=edc_notification_admin)
class NotificationAdmin(TemplatesModelAdminMixin, admin.ModelAdmin):
    model = Notification

    list_display = ("name", "display_name", "mailing_list_address")
