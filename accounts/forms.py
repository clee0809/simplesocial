from django.contrib.auth import get_user_model #https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#django.contrib.auth.get_user_model
from django.contrib.auth.forms import UserCreationForm # https://docs.djangoproject.com/en/4.0/topics/auth/default/#module-django.contrib.auth.forms

class UserCreateForm(UserCreationForm):
  class Meta:
    fields = ('username', 'email', 'password1', 'password2')
    model = get_user_model()

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.fields['username'].label = "Display Name"
    self.fields['email'].label = 'Email Address'
