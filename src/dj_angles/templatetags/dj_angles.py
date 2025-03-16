from datetime import date, datetime, time

from django import template

from dj_angles.templatetags.call import do_call
from dj_angles.templatetags.model import do_model

register = template.Library()


@register.filter(name="dateformat")
def dateformat(value: datetime | date | time, date_format: str):
    return value.strftime(date_format)


# Register custom template tags
register.tag("call", do_call)
register.tag("model", do_model)
