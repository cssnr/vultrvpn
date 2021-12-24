import logging
from django import template
from django.conf import settings
from django.templatetags.static import static

logger = logging.getLogger('app')
register = template.Library()


@register.simple_tag(name='get_config')
def get_config(value):
    return getattr(settings, value, None)


@register.filter(name='get_scheme')
def get_scheme(meta):
    if 'HTTP_X_FORWARDED_PROTO' in meta:
        return meta['HTTP_X_FORWARDED_PROTO']
    if 'HTTP_REFERER' in meta:
        return meta['HTTP_REFERER'].split(':')[0]
    return 'http'


@register.filter(name='tag_to_class')
def tag_to_class(value):
    return {
        'info': 'primary',
        'success': 'success',
        'warning': 'warning',
        'error': 'danger',
    }[value]


@register.filter(name='theme_css')
def theme_css(value=None):
    if not value or value == 'light':
        return 'bootstrap/css/bootstrap.min.css'
    else:
        return 'bootstrap/css/cyborg.min.css'


@register.filter(name='avatar_url')
def avatar_url(avatar_hash, username):
    if avatar_hash:
        return f'https://cdn.discordapp.com/avatars/{ username }/{ avatar_hash }.png'
    else:
        return static('images/assets/default-user.png')
