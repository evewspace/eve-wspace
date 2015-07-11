from django import template

register = template.Library()

@register.inclusion_tag('render_question.html', takes_context=True)
def render_question(context, question):
    context['question'] = question
    return context

@register.inclusion_tag('render_question.html', takes_context=True)
def render_edit_question(context, question):
    context['question'] = question
    context['edit_mode'] = True
    return context
    
@register.inclusion_tag('recruiter_render_question.html', takes_context=True)
def render_view_question(context, question, response):
    context['question'] = question
    context['response'] = response
    return context

@register.filter(name='key')
def key(d, key_name):
    try:
        value = d[key_name]
    except KeyError:
        from django.conf import settings

        value = settings.TEMPLATE_STRING_IF_INVALID

    return value