from datetime import date, datetime, time

from django import template

from dj_angles.templatetags.call import do_call
from dj_angles.templatetags.model import do_model
from dj_angles.templatetags.template import do_template

register = template.Library()


@register.filter(name="dateformat")
def dateformat(value: datetime | date | time, date_format: str):
    return value.strftime(date_format)


@register.inclusion_tag("dj_angles/scripts.html")
def dj_angles_scripts(*, ajax_form: bool = True):
    return {"ajax_form": ajax_form}


# Register custom template tags
register.tag("call", do_call)
register.tag("model", do_model)
register.tag("template", do_template)
