from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


def actions_buttons(model_instance):
    pass
    edit_url = reverse('admin:%s_%s_change' % (model_instance._meta.app_label, model_instance._meta.model_name), args=[model_instance.pk])
    delete_url = reverse('admin:%s_%s_delete' % (model_instance._meta.app_label, model_instance._meta.model_name), args=[model_instance.pk])

    return format_html('<a class="button" style="padding: 6px 12px; text-align: center; width: 80px; ; background-color: #206c91;" href="{}">EDIT</a>\
                        &nbsp;\
                        <a class="button" style="padding: 6px 12px; text-align: center; width: 80px; background-color: #dc3545; color: #fff;" href="{}">DELETE</a>'
                        .format(edit_url, delete_url))

def actions_buttons_edit(model_instance):
    pass
    edit_url = reverse('admin:%s_%s_change' % (model_instance._meta.app_label, model_instance._meta.model_name), args=[model_instance.pk])

    return format_html('<a class="button" style="padding: 6px 12px; text-align: center; width: 80px; ; background-color: #206c91;" href="{}">EDIT</a>\
                        &nbsp;'
                        .format(edit_url))

def actions_buttons_revoke(model_instance):
    delete_url = reverse('admin:%s_%s_delete' % (model_instance._meta.app_label, model_instance._meta.model_name), args=[model_instance.pk])

    return format_html('<a class="button" style="padding: 6px 12px; text-align: center; width: 80px; background-color: #dc3545; color: #fff;" href="{}">REVOKE</a>\
                        &nbsp;'
                        .format(delete_url))

actions_buttons.allow_tags = True
actions_buttons.short_description = 'Actions'

