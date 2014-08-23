from django import template
from django.template.defaultfilters import stringfilter

from projects.services import SkillService

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
@stringfilter
def strip(value):
    return value.strip()

@register.inclusion_tag('_skills_picker.html', takes_context=True)
def skills_picker(context, selection=None):
    service = SkillService()
    skills_options = service.all_grouped_as_picker_options()
    context["skills_options"] = skills_options
    return {
        "skills_options": skills_options,
        "selection": selection
    }

@register.filter
@stringfilter
def uniquelines(content):
    lines = content.split("\n")
    unique_lines = []
    for l in lines:
        l = l.strip()
        if l not in unique_lines:
            unique_lines.append(l)
    return "\n".join(unique_lines)
