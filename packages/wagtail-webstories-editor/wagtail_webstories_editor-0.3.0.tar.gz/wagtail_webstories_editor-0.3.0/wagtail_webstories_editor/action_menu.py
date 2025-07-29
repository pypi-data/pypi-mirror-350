from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.action_menu import ActionMenuItem
from wagtail.snippets.permissions import get_permission_name


class DeleteMenuItem(ActionMenuItem):
    name = "action-delete"
    label = _("Delete")
    icon_name = "bin"
    
    def __init__(self, order=None):
        super().__init__(order)
    
    def is_shown(self, context):
        delete_permission = get_permission_name("delete", context["model"])
        
        return (
                context["view"] == "edit"
                and context["request"].user.has_perm(delete_permission)
                and not context.get("locked_for_user")
        )
    
    def get_url(self, context):
        instance = context["instance"]
        url_name = instance.snippet_viewset.get_url_name("delete")
        return reverse(url_name, args=[quote(instance.pk)])
