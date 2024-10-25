from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="svg_icon")
def svg_icon(value):
    match value:
        case "success":
            return mark_safe(
                '<i class="fa-regular fa-circle-check"></i>'
            )

        case "error":
            return mark_safe(
                '<i class="fa-regular fa-circle-xmark"></i>'
            )

        case _:
            return ""
