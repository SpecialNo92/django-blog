from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from ..models import Tag
from ..utils import CustomListViewMixin


class TagDetail(CustomListViewMixin, View):
    """
    View posts with specified tag
    """
    template_name = 'blog/tag_detail.html'
    model = Tag
    paginate_by = 2
    context_list_name = 'post_list'
    context_object_name = 'tag'

    def get_queryset(self, **kwargs):
        user = kwargs.get('request').user
        detail_object = self.get_detail_object()

        if user.is_superuser is True:
            queryset = detail_object.blog_posts.all()
        else:
            queryset = detail_object.blog_posts.published()

        return queryset

    def get(self, request, slug):
        self.set_detail_object(get_object_or_404(self.model, slug__iexact=slug))
        context = self.get_context(**{'request': request})

        return render(request, self.template_name, context)
