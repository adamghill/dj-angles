from django import template

from dj_angles.templatetags.call import do_call
from dj_angles.templatetags.model import do_model

register = template.Library()


register.tag("call", do_call)
register.tag("model", do_model)
