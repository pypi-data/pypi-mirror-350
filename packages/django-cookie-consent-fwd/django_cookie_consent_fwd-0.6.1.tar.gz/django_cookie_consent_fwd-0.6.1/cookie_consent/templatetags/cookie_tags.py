from django import template
from cookie_consent.conf import settings
from cookie_consent.util import get_cookie_groups
from cookie_consent.models import CookieGroup

register = template.Library()

@register.simple_tag
def load_cookie_groups():
    cookie_groups = get_cookie_groups()
    return [group.varname for group in cookie_groups]

@register.simple_tag
def show_cookie_names_in_modal():
    return getattr(settings, 'SHOW_COOKIE_NAMES_IN_MODAL', False)