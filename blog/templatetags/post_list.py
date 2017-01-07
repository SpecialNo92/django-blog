from django import template

from ..models import (Post)

register = template.Library()


@register.inclusion_tag('blog/includes/partial_post_list.html', takes_context=True)
def default_post_list(context, specify_list=None):
    """
    Print post list from "post_list" context variable, unless specify_list is specified
    """
    request = context.get('request')
    #
    # if request.user.is_superuser is True:
    #     post_list = detail_object.blog_posts.all()
    # else:
    #     post_list = detail_object.blog_posts.published()


    if specify_list is None:
        pass
    else:
        context.update({'post_list': specify_list})

    return context
