from django import template

register = template.Library()

@register.filter
def get_platform(metrics_queryset, platform):
    return metrics_queryset.filter(platform=platform).first() 