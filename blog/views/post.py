from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import View, ListView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from user.utils import RequireAuthenticatedPermission
from ..models import Post
from ..forms import PostForm, CommentForm
from ..utils import CustomListViewMixin


class PostList(CustomListViewMixin, View):
    template_name = 'blog/post_list.html'
    paginate_by = 2
    context_list_name = 'post_list'

    def get_queryset(self, **kwargs):
        user = kwargs.get('request').user
        if user.is_superuser is True:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.published()

        return queryset

    def get(self, request):
        context = self.get_context(**{'request': request})

        return render(request, self.template_name, context)


class PostCreate(RequireAuthenticatedPermission, View):
    """
    Create new entry, requires authorized access and 'blog.user_add_his_post' permissions
    After success redirect to just created object with message
    """
    permission_required = 'blog.add_post'
    raise_exception = False
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_msg = 'Successfully created new post!'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST, request.FILES)
        if bound_form.is_valid():
            new_obj = bound_form.save(**{'request': request})
            messages.success(request, self.success_msg)
            return redirect(reverse('blog_post_detail', kwargs={'pk': new_obj.pk, 'slug': new_obj.slug}))

        return render(request, self.template_name, {'form': bound_form})


class PostDetail(View):
    """
    Show post, and if logged show also form to add comment
    If form submitted on success view message and redirect to same webpage (to clear POST) with message
    """
    template_name = 'blog/post_detail.html'
    form_class = CommentForm
    comment_success_msg = 'Successfully added new comment'
    model = Post

    def get(self, request, pk, slug):
        context = {
            'post': get_object_or_404(self.model, pk=pk),
            'form': self.form_class()
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, pk, slug):
        bound_comment_form = self.form_class(request.POST)

        if bound_comment_form.is_valid():
            bound_comment_form.save(**{'request': request, 'post_pk': pk})
            messages.success(request, self.comment_success_msg)
            return redirect(reverse('blog_post_detail', kwargs={'pk': pk, 'slug': slug}))


        context = {
            'post': get_object_or_404(self.model, pk=pk),
            'form': bound_comment_form
        }
        return render(request, self.template_name, context)


class PostUpdate(RequireAuthenticatedPermission, View):
    """
    Allows someone with permission edit Posts, after success redirect to updated post with message
    """
    permission_required = 'blog.edit_post'
    template_name = 'blog/post_form_update.html'
    success_message = "Successfully edited post!"
    form_class = PostForm
    model = Post

    def get(self, request, pk, slug):
        get_instance = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'form': self.form_class(instance=get_instance)})

    def post(self, request, pk, slug):
        get_instance = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, request.FILES, instance=get_instance)

        if bound_form.is_valid():
            updated_obj = bound_form.save()
            messages.success(request, self.success_message)
            return redirect(reverse('blog_post_detail', kwargs={'pk': updated_obj.pk, 'slug': updated_obj.slug}))

        return render(request, self.template_name, {'form': bound_form})


class PostDelete(RequireAuthenticatedPermission, View):
    """
    Allows someone with permission delete Posts
    """
    permission_required = 'blog.remove_post'
    template_name = 'blog/post_confirm_delete.html'
    success_message = "Successfully deleted post!"
    success_url = reverse_lazy('blog_post_list')
    model = Post

    def get(self, request, pk, slug):
        return render(request, self.template_name, {})

    def post(self, request, pk, slug):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()

        messages.success(request, self.success_message)
        return redirect(self.success_url)