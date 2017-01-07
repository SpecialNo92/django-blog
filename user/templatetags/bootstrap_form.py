from django import template

register = template.Library()


@register.inclusion_tag('includes/form_snippet.html', takes_context=True)
def bootstrap_form(context, specify_form=None):
    """
    By default does looks for 'form' key in context,
        unless specify_form is specified, then ignores context and print form
    """
    if specify_form is None:
        form = context.get('form')
    else:
        form = specify_form

    return {
        'form': form
    }


@register.filter(name='addcss')
def addcss(value, arg):
    """
    Adds css attributes to given field
    """
    css_classes = value.field.widget.attrs.get('class', '').split(' ')
    if css_classes and arg not in css_classes:
        css_classes = '%s %s' % (css_classes, arg)
    return value.as_widget(attrs={'class': css_classes})