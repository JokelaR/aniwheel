from django import template
from datetime import date as Date
import html

register = template.Library()

@register.filter
def date(date: Date):
    return date.strftime('%d %B, %Y').lstrip('0')

@register.filter
def unescape(string: str):
    return html.unescape(string)