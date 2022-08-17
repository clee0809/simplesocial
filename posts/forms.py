from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "group", 'image')
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["group"].queryset = (
                models.Group.objects.filter(
                    pk__in=user.groups.values_list("group__pk")
                )
            )

class CommentForm(forms.ModelForm):
    class Meta():
        model = models.Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea commentcontent'})
        }
