from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustomListViewMixin:
    """
    Use it to print lists or print detailed object with lists
    Set and get your detailed object with set_detail_object(obj), and get_detail_object()
    For fetching QuerySet use method get_queryset(**kwargs) or queryset_list field ( only for simple ones )

    Context is only updated, so you can pass any context you want to get_context method

    fields:
        paginate_by - Set number of items to paginate by, or leave None for no pagination
        context_list_name - what name your list will be in context and templates
        context_object_name - what name your detailed object will be in context and templates
    """
    paginate_by = None
    queryset_list = None
    context_list_name = 'object_list'

    _detail_object = None
    context_object_name = 'detail_object'

    def set_detail_object(self, obj):
        self._detail_object = obj

    def get_detail_object(self):
        return self._detail_object

    def get_queryset(self, **kwargs):
        return self.queryset_list

    def get_page_size(self):
        return self.paginate_by

    def paginated(self, **kwargs):
        queryset = self.get_queryset(**kwargs)

        if self.get_page_size() is None:
            return queryset

        request = kwargs.get('request')
        page = request.GET.get('page', 1)

        paginator = Paginator(queryset, self.get_page_size())

        try:
            paginated_query = paginator.page(page)
        except PageNotAnInteger:
            paginated_query = paginator.page(1)
        except EmptyPage:
            paginated_query = paginator.page(paginator.num_pages)

        return paginated_query

    def grab_paginated_context(self, context, **kwargs):
        paginated_queryset = self.paginated(**kwargs)

        if self.get_page_size():
            context.update({
                'is_paginated': True,
                'page_obj': paginated_queryset,
            })
        else:
            context.update({
                'is_paginated': False,
                'page_obj': None,
            })

        context.update({
            self.context_list_name: paginated_queryset,
        })

        return context

    def grab_object_context(self, context, **kwargs):
        if self.get_detail_object() is not None:
            context.update({
                    self.context_object_name: self.get_detail_object()
            })
            return context

    def get_context(self, context=None, **kwargs):
        if context is None:
            context = {}

        self.grab_object_context(context, **kwargs)
        self.grab_paginated_context(context, **kwargs)

        return context



