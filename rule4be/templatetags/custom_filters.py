from django import template
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime

register = template.Library()

@register.filter
def relative_date(value):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    last_week = today - datetime.timedelta(days=7)
    last_month = today - relativedelta(months=1)
    last_year = today - relativedelta(years=1)

    if value == today:
        return "Today"
    elif value == yesterday:
        return "Yesterday"
    elif value == last_week:
        return "Last week"
    elif value == last_month:
        return "Last month"
    elif value == last_year:
        return "Last Year"
    else:
        return value
    
@register.filter(name='custom_title')
def custom_title(value):
    return value.replace('_', ' ').title()

@register.filter
def first_letter(value):
    return value[0] if value else ''