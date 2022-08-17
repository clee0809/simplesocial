#  POSTS VIEWS.PY

from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import Http404, HttpResponse, HttpResponseRedirect
# pip install django-braces
from braces.views import SelectRelatedMixin
from django.contrib import messages
import datetime


from . import models
from . import forms
from groups.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
# list of posts related either 'user' or 'group' or both, Post model has 'user' and 'group'
class PostList(SelectRelatedMixin, generic.ListView):
  paginate_by = 4
  model = models.Post
  select_related = ('user', 'group') # https://django-braces.readthedocs.io/en/latest/other.html#selectrelatedmixin
  queryset = models.Post.objects.all()


  def get_context_data(self, **kwargs):    
    context = super().get_context_data(**kwargs)
    context['now'] = datetime.datetime.now()
    context['all_groups'] = Group.objects.all()
    return context

  

# list view for a specific user's posts
class UserPosts(generic.ListView):
  model = models.Post
  template_name = 'posts/user_post_list.html'

  def get_queryset(self):
    try:
      # 18:37 184
      # user that belongs to this particular post equal to user that users objects
      self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
    except User.DoesNotExist:
      raise Http404
    else:
      return self.post_user.posts.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print(context['object_list'])
    print(self.model.image)
    context['post_user'] = self.post_user
    return context

class PostDetail(SelectRelatedMixin, generic.DetailView):
  model = models.Post
  select_related = ('user', 'group')

  def get_queryset(self):
    queryset = super().get_queryset()
    
    # https://www.dev2qa.com/what-does-double-underscore-__-means-in-django-model-queryset-objects-filter-method/
    # User Double Underscore ( __ ) To Reference Foreign Key Model Class’s Attribute.
    # user: Post user attribute, username: User attribute
    # you can use double underscore to separate the foreign key user and it’s attribute username in the filter method.
    return queryset.filter(user__username__iexact = self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
  fields = ('message', 'group', 'image')
  model = models.Post
  
  # If the form is valid, redirect to the supplied URL
  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    try:
      self.object.save()

    except IntegrityError:      
      messages.warning(self.request, "Same message already posted.")
      return HttpResponseRedirect(reverse("posts:all"))
      
    return super().form_valid(form)


class EditPost(LoginRequiredMixin, generic.UpdateView):
  model = models.Post
  fields = ('message', 'image')
  template_name_suffix = '_update_form'  


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
  model = models.Post
  select_related = ('user', 'group')
  success_url = reverse_lazy('posts:all')

  def get_queryset(self):
    queryset= super().get_queryset()
    return queryset.filter(user_id=self.request.user.id) # TODO user_id ?

  def delete(self, *args, **kwargs):
    messages.success(self.request, 'Post Deleted')
    return super().delete(*args, **kwargs)


