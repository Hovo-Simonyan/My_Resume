from django import template
from django.db.models import Count

from ..models import *


register = template.Library()


@register.simple_tag()
def get_languages():
    return Language.objects.annotate(cnt=Count('resume')).filter(cnt__gt=0)

