import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def render_markdown(value):
    result = md.markdown(value, extensions=["tables", "nl2br"])
    return mark_safe(result)
